"""Opt-in typed remote collection, grants checked before every acquisition.

Generic JSON/RSS/OAI adapters, not provider-specific certified integrations.
Never treats metadata as a full document or a feed as proof of rights.
"""
from __future__ import annotations
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qsl
import json
from typing import Any

from .model import BridgeError, SourceItem, Rights, Limits, utcnow, digest
from .registry import AccessPlanner, SourceRegistry, CapabilityGrant
from .ingest import LocalIngestor, xml_safe, local_name
from .network import Transport, get_paginated_json


def collect_json(url:str,platform_id:str,grant:CapabilityGrant,client:Transport,
                 *,max_pages:int=5,max_records:int=200)->LocalIngestor:
    _admit(platform_id,grant,'api_read')
    records,history=get_paginated_json(client,url,max_pages=max_pages,max_records=max_records)
    ing=LocalIngestor()
    for ix,record in enumerate(records):
        # Generic API records are structured metadata, not full article text.
        eid=str(record.get('id',record.get('doi',record.get('DOI',ix))))[:500]
        src=SourceItem(platform_id,eid,history[-1].get('etag','') or 'api-snapshot-'+digest(record)[:16],
                       'structured_record',grant.rights,acquired_via='api_read')
        ing.add_text(source=src,text=json.dumps(record,ensure_ascii=False,sort_keys=True),
                     locator=f'api-record:{ix}',quote_verified=False)
    ing.corpus.warnings.append('api_json_metadata_only_provider_contract_not_certified')
    return ing


def collect_feed(url:str,platform_id:str,grant:CapabilityGrant,client:Transport,
                 *,mode:str='rss_atom',max_items:int=100)->LocalIngestor:
    if mode not in {'rss_atom','harvest_oai_pmh'}:
        raise BridgeError('METHOD_UNSUPPORTED','Only RSS/Atom/OAI read supported')
    _admit(platform_id,grant,mode)
    status,headers,payload=client.get(url)
    if len(payload)>2_000_000:
        raise BridgeError('NETWORK_LIMIT','Feed exceeds 2 MB')
    if status!=200:
        raise BridgeError('NETWORK_STATUS','Full successful feed response required')
    root=xml_safe(payload)
    nodes=[x for x in root.iter() if local_name(x.tag) in ('item','entry','record')]
    if len(nodes)>max_items or max_items>1000:
        raise BridgeError('NETWORK_LIMIT','Too many feed items')
    ing=LocalIngestor()
    for ix,node in enumerate(nodes):
        item={}
        for child in node.iter():
            if child is node:continue
            key=local_name(child.tag)
            if key in ('title','identifier','id','guid','link','description','summary','abstract','creator','date','published'):
                val=(child.text or '').strip()
                if val and key not in item:item[key]=val[:15000]
                if key=='link' and not val and 'href' in child.attrib:
                    item['link']=child.attrib['href'][:1500]
        eid=item.get('identifier') or item.get('id') or item.get('guid') or item.get('link') or f'feed-item:{ix}'
        # Feed text is metadata/abstract only. Even if content:encoded contains long body,
        # it is deliberately not treated as an authorized full article.
        kind='abstract' if (item.get('abstract') or item.get('description') or item.get('summary')) else 'structured_record'
        revision=headers.get('etag') or headers.get('last-modified') or digest(item)[:24]
        src=SourceItem(platform_id,str(eid)[:600],str(revision)[:1200],kind,grant.rights,
                       title=item.get('title','')[:300],acquired_via=mode)
        ing.add_text(source=src,text=json.dumps(item,ensure_ascii=False,sort_keys=True),
                     locator=f'{mode}-record:{ix}',quote_verified=False)
    ing.corpus.warnings.append(mode+': metadata_and_summaries_only_no_full_text_claim')
    return ing


def _admit(platform_id:str,grant:CapabilityGrant,mode:str):
    profile=SourceRegistry().get(platform_id)
    if not any(a['mode']==mode and a['doc_status']=='official_docs_checked' for a in profile['access_paths']):
        raise BridgeError('PROVIDER_UNVERIFIED','Network provider method is not verified in registry')
    if grant.platform_id!=platform_id or grant.method!=mode or not grant.host_approved or not grant.owner_contract_ref:
        raise BridgeError('OWNER_ADMISSION','Host and owner contract required for remote method')
    if not grant.implementation_tested:
        raise BridgeError('ADAPTER_UNTESTED','Remote route is not enabled for this scope')
    if not grant.rights.allowed('read') or not grant.rights.allowed('copy') or not grant.rights.allowed('transform'):
        raise BridgeError('RIGHTS_DENIED','Remote import requires read/copy/transform rights')


def collect_oai_pages(url:str,platform_id:str,grant:CapabilityGrant,client:Transport,
                      *,max_pages:int=8,max_records:int=500)->LocalIngestor:
    """Bounded OAI-PMH ListRecords incl. resumption tokens; metadata-only output.

    OAI endpoint and metadataPrefix must be preconfigured by the owner, not guessed.
    The tokens never authorize full-text acquisition or downstream sharing.
    """
    _admit(platform_id,grant,'harvest_oai_pmh')
    if not 1<=max_pages<=30 or not 1<=max_records<=2000:
        raise BridgeError('NETWORK_LIMIT','OAI bounds exceeded')
    from .ingest import xml_safe,local_name
    parts=urlsplit(url)
    if parts.scheme!='https' or not parts.hostname or 'verb=ListRecords' not in parts.query:
        raise BridgeError('OAI_URL','Explicit HTTPS ListRecords endpoint required')
    seen=set();collected=0;ing=LocalIngestor()
    for page in range(max_pages):
        if url in seen: raise BridgeError('OAI_PAGINATION','Repeated OAI URL')
        seen.add(url)
        status,headers,payload=client.get(url)
        if status!=200 or len(payload)>2_000_000:
            raise BridgeError('OAI_RESPONSE','OAI endpoint failed or oversized')
        root=xml_safe(payload)
        if any(local_name(x.tag)=='error' for x in root.iter()):
            raise BridgeError('OAI_PROVIDER_ERROR','OAI provider reported an error')
        for record in (x for x in root.iter() if local_name(x.tag)=='record'):
            collected+=1
            if collected>max_records: raise BridgeError('NETWORK_LIMIT','OAI item cap exceeded')
            entry={}
            for node in record.iter():
                key=local_name(node.tag)
                if key in ('identifier','title','creator','date','subject','description','publisher','type'):
                    value=(node.text or '').strip()
                    if value: entry.setdefault(key,[]).append(value[:1200])
            # OAI delete markers are represented as references only.
            is_deleted=any(local_name(h.tag)=='header' and h.attrib.get('status')=='deleted' for h in record)
            if not entry: continue
            identifier=entry.get('identifier',[f'oai:{page}:{collected}'])[0]
            revision=headers.get('etag') or digest((identifier,entry))[:24]
            item=SourceItem(platform_id,identifier,revision,'reference_only' if is_deleted else 'structured_record',
                            grant.rights,acquired_via='harvest_oai_pmh')
            if is_deleted: ing.add_reference(item)
            else: ing.add_text(source=item,text=json.dumps(entry,sort_keys=True,ensure_ascii=False),
                               locator=f'oai:page:{page}:record:{collected}',quote_verified=False)
        tokens=[(x.text or '').strip() for x in root.iter() if local_name(x.tag)=='resumptiontoken']
        token=tokens[-1] if tokens else ''
        if not token:break
        if len(token)>1000:raise BridgeError('OAI_PAGINATION','Unsafe resumption token length')
        # OAI-PMH next requests contain only verb + resumptionToken. Keep same host.
        query=urlencode({'verb':'ListRecords','resumptionToken':token})
        url=urlunsplit((parts.scheme,parts.netloc,parts.path,query,''))
    else:
        if token:ing.corpus.warnings.append('oai_incomplete_max_pages_reached')
    ing.corpus.warnings.append('oai_metadata_only_no_source_bytes_permission')
    return ing
