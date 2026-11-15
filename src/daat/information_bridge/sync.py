"""Tenant-bound metadata checkpoints and source revision/dedup previews.

This is *not* a parallel Orgo job scheduler or Médiathèque source custody store.
"""
from __future__ import annotations
from pathlib import Path
import json
import sqlite3
import time
import hashlib
from typing import Any
from .model import BridgeError, digest

class Checkpoints:
    def __init__(self,path:Path,tenant:str):
        if not tenant or len(tenant)>128: raise BridgeError('TENANT_INVALID','Tenant required')
        self.path=Path(path);self.tenant=tenant
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with self._db() as con:
            con.execute('''CREATE TABLE IF NOT EXISTS checkpoints(
                 tenant TEXT NOT NULL, job_key TEXT NOT NULL, source_ref TEXT NOT NULL,
                 revision TEXT NOT NULL, cursor TEXT, state TEXT NOT NULL,
                 metadata_sha256 TEXT NOT NULL, PRIMARY KEY (tenant,job_key,source_ref))''')
            con.execute('''CREATE TABLE IF NOT EXISTS seen(
                 tenant TEXT NOT NULL, identity TEXT NOT NULL, revision TEXT NOT NULL,
                 payload_hash TEXT NOT NULL, PRIMARY KEY (tenant,identity,revision))''')

    def _db(self):
        return sqlite3.connect(self.path,timeout=10)

    def put(self,job_key:str,source_ref:str,revision:str,cursor:str|None,
            state:str='REFERENCED',metadata:dict[str,Any]|None=None):
        if state not in ('DRAFT','REFERENCED','NORMALIZED','CONTEXT_READY','BLOCKED','RETRYABLE','EFFECT_UNKNOWN','REVOKED'):
            raise BridgeError('CHECKPOINT_INVALID','Unknown local state')
        if any(not x or len(x)>300 for x in (job_key,source_ref,revision)) or (cursor and len(cursor)>1000):
            raise BridgeError('CHECKPOINT_INVALID','Unbounded checkpoint key')
        # metadata values themselves not persisted: only a digest. Tokens must never be cursors.
        if cursor and any(x in cursor.lower() for x in ('token=', 'apikey=', 'password=', 'secret=')):
            raise BridgeError('CHECKPOINT_SECRET','Potential secret in cursor')
        sig=digest(metadata or {})
        with self._db() as con:
            previous=con.execute('''SELECT revision,state FROM checkpoints WHERE tenant=? AND job_key=? AND source_ref=?''',
                (self.tenant,job_key,source_ref)).fetchone()
            if previous and previous[1]=='REVOKED' and state != 'REVOKED':
                raise BridgeError('CHECKPOINT_REVOKED','Cannot revive revoked source without owner renewal')
            con.execute('''INSERT INTO checkpoints VALUES(?,?,?,?,?,?,?)
                      ON CONFLICT(tenant,job_key,source_ref) DO UPDATE SET revision=excluded.revision,
                      cursor=excluded.cursor,state=excluded.state,metadata_sha256=excluded.metadata_sha256''',
                      (self.tenant,job_key,source_ref,revision,cursor,state,sig))

    def get(self,job_key:str,source_ref:str)->dict[str,str]|None:
        with self._db() as con:
            row=con.execute('''SELECT revision,cursor,state,metadata_sha256 FROM checkpoints
                WHERE tenant=? AND job_key=? AND source_ref=?''',(self.tenant,job_key,source_ref)).fetchone()
        if row is None:return None
        return dict(zip(('revision','cursor','state','metadata_sha256'),row))

    def observe(self,identity:str,revision:str,payload:dict[str,Any])->str:
        if not identity or not revision: raise BridgeError('IDENTITY_INVALID','Identity and revision required')
        sha=digest(payload)
        with self._db() as con:
            row=con.execute('SELECT payload_hash FROM seen WHERE tenant=? AND identity=? AND revision=?',
                            (self.tenant,identity,revision)).fetchone()
            if row:
                return 'duplicate' if row[0]==sha else 'revision_conflict'
            con.execute('INSERT INTO seen VALUES(?,?,?,?)',(self.tenant,identity,revision,sha))
            return 'new'


def identify_duplicates(sources:list[Any])->dict[str,Any]:
    """Exact same source revision vs candidate DOI/URL; no semantic identity assertion."""
    exact={}; suggestions={}; result={'exact':[],'review_candidates':[]}
    for source in sources:
        key=(source.platform_id,source.external_id,source.revision)
        if key in exact:result['exact'].append((exact[key],source.ref()))
        else:exact[key]=source.ref()
        external=source.external_id.lower().strip()
        if external.startswith('https://doi.org/'):
            external=external.removeprefix('https://doi.org/')
        if external.startswith('doi:'):
            external=external[4:]
        if external.startswith('10.') and '/' in external:
            if external in suggestions and suggestions[external]!=source.ref():
                result['review_candidates'].append({'kind':'same_doi_candidate',
                             'refs':[suggestions[external],source.ref()],'canonical_match':False})
            else:suggestions[external]=source.ref()
    return result
