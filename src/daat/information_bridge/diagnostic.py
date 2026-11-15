"""Evidence-oriented local diagnostic report for DaaT bridge, not certification."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
from typing import Any
from .registry import SourceRegistry, LOCAL_METHODS, NETWORK_METHODS
from .model import utcnow
from .context import verify_export


def readiness(export:Path|None=None)->dict[str,Any]:
    registry=SourceRegistry()
    profiles=list(registry.profiles.values())
    methods=sorted({a['mode'] for p in profiles for a in p['access_paths']})
    official=[p['id'] for p in profiles if p['platform_doc_status']=='official_docs_checked']
    status=[]
    for p in profiles:
        status.append({'platform_id':p['id'],'family_ids':p['family_ids'],
             'provider_docs_checked':p['platform_doc_status']=='official_docs_checked',
             'local_generic_routes':[a['mode'] for a in p['access_paths'] if a['mode'] in LOCAL_METHODS],
             'network_generic_routes':[a['mode'] for a in p['access_paths'] if a['mode'] in NETWORK_METHODS],
             'owner_connector_certified':False,'source_rights_granted':False})
    report={'schema':'daat.information-bridge-readiness/1.0-local',
        'generated_at':utcnow(), 'result':'NOT_PRODUCTION_QUALIFIED',
        'registry':{'profiles':len(profiles),'families':len(registry.families),
                    'official_docs_profiles':len(official),'unverified_docs_profiles':len(profiles)-len(official),
                    'access_methods':methods},'platforms':status,
        'components':{'local_ingestion':'implemented_with_synthetic_tests',
           'remote_https':'implemented_opt_in_not_provider_certified',
           'context_bundle':'implemented_local_proposed_schema',
           'manual_chatgpt':'implemented_no_api_transfer',
           'producer_owner_contracts':'not_adopted',
           'live_source_validation':'not_executed',
           'kristal_authoring':'out_of_scope',
           'windows_gui':'not_visually_certified'},
        'limitations':['External accounts/licenses unavailable; no live connector qualification.',
                       'Source rights attestations do not prove owner authority.',
                       'Context bundles are unsigned local preparation artifacts.',
                       'The source registry is research material, not an access grant.']}
    if export is not None:
        try:report['export_verification']=verify_export(export)
        except Exception as exc: report['export_verification']={'valid':False,'error_code':getattr(exc,'code','VERIFY_ERROR')}
    return report
