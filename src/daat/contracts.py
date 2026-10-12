"""Pinned, strictly offline validators using unchanged IK-owner JSON Schemas."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
from .errors import ContractError
from .util import file_digest,load_json

# Caller may supply another checked-out exact owner baseline.
_REPO_OWNERS=Path(__file__).resolve().parents[2]/'contracts'/'owners'/'ik'
_BUNDLED_OWNERS=Path(__file__).resolve().parent/'resources'/'contracts'/'owners'/'ik'
OWNERS=_REPO_OWNERS if _REPO_OWNERS.is_dir() else _BUNDLED_OWNERS
ALIASES={
  'envelope':'envelope.schema.json','receipt':'receipt.schema.json',
  'artifact-ref':'artifact-ref.schema.json','export-manifest':'export-manifest.schema.json',
  'build':'profiles/kristal/kristal.build.request/2.0.0/payload.schema.json',
  'ready':'profiles/kristal/kristal.artifact.ready/2.0.0/payload.schema.json'
}

def verify_baseline(root: Path=OWNERS) -> dict:
    meta=load_json(root/'SHA256SUMS.json')
    expected=meta['files']
    for relative,pinned in expected.items():
        p=(root/relative).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file() or file_digest(p)!=pinned:
            raise ContractError('CONTRACT_PIN_MISMATCH',f'Pinned owner file mismatch: {relative}')
    if set(p.relative_to(root).as_posix() for p in root.rglob('*.json') if p.name!='SHA256SUMS.json')!=set(expected):
        raise ContractError('CONTRACT_PIN_MISMATCH','Owner contract files added or removed')
    lock=load_json(root/'kristal.lock.json')
    if lock['version']!='6.0.0' or lock['format']!='kristal.consumer-lock/v2' or lock['canonicalization_profile']!='kristal.v6:jcs-rfc8785':
        raise ContractError('UNSUPPORTED_CONTRACT_VERSION','Kristal v6 lock mismatch')
    return {'baseline':'verified','files':len(expected),'kristal_contract_set':lock['version'],
            'v7_design_note':'IK v7 draft.3.1 vs Kristal draft.3.2; no automatic reconciliation'}

def validate_owner(kind: str, obj: Any, root: Path=OWNERS) -> None:
    verify_baseline(root)
    if kind not in ALIASES: raise ContractError('UNKNOWN_SCHEMA','Unknown IK schema alias')
    all_schemas=[]
    for p in root.rglob('*.schema.json'):
        doc=load_json(p)
        if '$id' in doc: all_schemas.append((doc['$id'],doc))
    reg=Registry()
    for uri,doc in all_schemas: reg=reg.with_resource(uri,Resource.from_contents(doc))
    schema=load_json(root/ALIASES[kind])
    validator=Draft202012Validator(schema, registry=reg, format_checker=FormatChecker())
    problems=list(validator.iter_errors(obj))
    if problems:
        err=sorted(problems,key=lambda e:(list(map(str,e.absolute_path)),e.message))[0]
        path='.'.join(map(str,err.absolute_path))
        raise ContractError('SCHEMA_INVALID',f'{kind} invalid at {path or "$"}: {err.message}')

def verify_payload_profile(envelope: dict, root: Path=OWNERS) -> None:
    validate_owner('envelope',envelope,root)
    if envelope.get('profile')!={'id':'kristal.build.request','version':'2.0.0'} or envelope.get('class')!='command':
        raise ContractError('UNKNOWN_PROFILE','Only IK Kristal build v2 command is approved')
    if envelope.get('target',{}).get('system')!='daat':
        raise ContractError('TARGET_MISMATCH','Build target must be daat')
    profile=load_json(root/'profiles/kristal/kristal.build.request/2.0.0/profile.json')
    if envelope.get('source',{}).get('system') not in profile['source_systems']:
        raise ContractError('UNAUTHORIZED_SOURCE_PROFILE','Source not approved by IK build profile')
    if not isinstance(envelope.get('authority'),dict) or envelope['authority'].get('kind') not in profile['authority']['accepted_kinds']:
        raise ContractError('AUTHORIZATION_DENIED','IK requires approved authority kind')
    if not envelope.get('idempotency_key') or not envelope.get('artifact_refs'):
        raise ContractError('MISSING_EXPORT','IK build requires idempotency and source artifact references')
    if envelope.get('response')!={'acceptance_receipt':True,'final_receipt':True,'outcome_events':['kristal.artifact.ready']}:
        raise ContractError('RECEIPT_POLICY_MISMATCH','IK build requires acceptance and final receipts plus outcome event')
    validate_owner('build',envelope.get('data'),root)
    if envelope['data']['requested_outputs']!=['kristal_state']:
        raise ContractError('UNSUPPORTED_OUTPUT','Reference bridge only knows the kristal_state completion stage')
