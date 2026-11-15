"""Read-only 89 platform registry and explicit, conservative access routing."""
from __future__ import annotations
import json
from pathlib import Path
from importlib.resources import files
from dataclasses import dataclass
from typing import Any
from .model import BridgeError, Rights, utcnow, digest

# These methods are local implementations; no other catalogue route is silently promoted.
LOCAL_METHODS = frozenset({'manual_paste','local_file','user_export','git_snapshot','federated_ref'})
NETWORK_METHODS = frozenset({'api_read','rss_atom','harvest_oai_pmh'})
METHOD_LANES = {'manual_paste':'L1','local_file':'L1','user_export':'L1',
                'git_snapshot':'L5','federated_ref':'L8',
                'api_read':'L2','rss_atom':'L3','harvest_oai_pmh':'L3',
                'bulk_export':'L4','licensed_batch':'L4','database_read':'L6','events':'L7',
                'authenticated_web':'L1'}

class SourceRegistry:
    def __init__(self, path: Path | None = None):
        if path is None:
            path = files('daat').joinpath('resources','data','platform-access-registry.v1.json')
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise BridgeError('REGISTRY_UNAVAILABLE', 'Source registry unavailable or invalid') from exc
        if data.get('schema') != 'koa.daat.platform-access-registry.v1':
            raise BridgeError('REGISTRY_INVALID','Unexpected registry version')
        profiles = data.get('platforms',[])
        if len(profiles) != 89 or len({p.get('id') for p in profiles}) != 89:
            raise BridgeError('REGISTRY_INVALID','Expected 89 distinct profiles')
        families = {str(f['id']) for f in data.get('families',[])}
        if len(families) != 36:
            raise BridgeError('REGISTRY_INVALID','Expected 36 families')
        for p in profiles:
            if not p.get('family_ids') or any(f not in families for f in p['family_ids']):
                raise BridgeError('REGISTRY_INVALID','Unknown platform family')
            modes = [a.get('mode') for a in p.get('access_paths',[])]
            if len(set(modes)) != len(modes) or any(m not in METHOD_LANES for m in modes):
                raise BridgeError('REGISTRY_INVALID','Unknown or repeated access mode')
        self.data = data
        self.profiles = {p['id']:p for p in profiles}
        self.families = families
        self.path = path

    def get(self, platform_id: str) -> dict[str,Any]:
        if platform_id not in self.profiles:
            raise BridgeError('UNKNOWN_PLATFORM', 'Platform has no registered profile')
        return dict(self.profiles[platform_id])

    def search(self, term: str='') -> list[dict[str,Any]]:
        q = term.casefold().strip()
        return [p for p in self.profiles.values() if q in
                (p['id'] + ' ' + p.get('platform','') + ' ' + p.get('information_scope','')).casefold()]

@dataclass(frozen=True)
class CapabilityGrant:
    """Owner/operator capability is out-of-band. A registry record never creates one."""
    platform_id: str
    method: str
    rights: Rights
    implementation_tested: bool = False
    host_approved: bool = False
    owner_contract_ref: str = ''
    bounded_endpoint: str = ''

    def __post_init__(self):
        if self.method not in METHOD_LANES:
            raise BridgeError('METHOD_UNSUPPORTED','Unknown access mode')

class AccessPlanner:
    def __init__(self, registry: SourceRegistry):
        self.registry = registry

    def plan(self, platform_id: str, grants: list[CapabilityGrant] | None = None,
             *, desired_kind: str = 'reference_only', allow_network: bool=False) -> dict[str,Any]:
        profile = self.registry.get(platform_id)
        grants = grants or []
        routes = []
        for access in profile['access_paths']:
            mode = access['mode']
            candidates = [g for g in grants if g.platform_id == platform_id and g.method == mode]
            grant = candidates[0] if candidates else None
            reasons = []
            if access['doc_status'] != 'official_docs_checked' and mode in NETWORK_METHODS:
                reasons.append('provider_documentation_unverified')
            if mode not in LOCAL_METHODS | NETWORK_METHODS:
                reasons.append('adapter_unimplemented_requires_owner')
            if mode in NETWORK_METHODS and not allow_network:
                reasons.append('network_not_enabled')
            if mode in NETWORK_METHODS and not (grant and grant.host_approved and grant.owner_contract_ref):
                reasons.append('host_or_owner_approval_absent')
            if mode == 'authenticated_web':
                reasons.append('no_browser_session_automation')
            if not grant:
                reasons.append('explicit_source_rights_absent')
            else:
                if not grant.rights.allowed('read'):
                    reasons.append('read_right_absent_or_expired')
                if not grant.implementation_tested:
                    reasons.append('adapter_not_tested_for_this_scope')
            if desired_kind != 'reference_only' and mode == 'federated_ref':
                reasons.append('reference_only_cannot_supply_text')
            status = 'eligible' if not reasons else 'blocked'
            routes.append({'method':mode, 'lane':METHOD_LANES[mode], 'status':status,
                           'documentation':access['doc_status'], 'reasons':reasons})
        eligible = [r for r in routes if r['status']=='eligible']
        preferred = profile.get('preferred_path')
        chosen = next((r for r in eligible if r['method'] == preferred), None)
        if chosen is None:
            chosen = eligible[0] if eligible else None
        return {'schema':'daat.source-access-decision/1.0-local-proposed',
                'decision_id':'access-'+digest((platform_id,desired_kind,routes))[:24],
                'profile_id':platform_id, 'profile_revision':self.registry.data['revision'],
                'desired_kind':desired_kind, 'selected_method':chosen['method'] if chosen else None,
                'result':'eligible' if chosen else 'blocked', 'methods_considered':routes,
                'full_text_access_implied':False, 'canonical_authority':False,
                'recommended_next_action':('use_verified_grant' if chosen else
                  'obtain_provider_permission_or_supply_authorized_export_or_reference'),
                'checked_at':utcnow()}
