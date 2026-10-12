"""Offline, explicitly host-trusted external mapping entrypoint.

Not an IK wire profile or HTTP endpoint. External messages are never admitted
based on client-provided `tenant`, `system` or `principal` alone.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Protocol
import json
from pathlib import Path
from .bridge import VerifiedPrincipal
from .errors import AdmissionError
from .mapping import load_profile,apply
from .security import SecurityGate,PolicyRequest,PolicyAuthority,AuditSink
from .util import json_digest

@dataclass(frozen=True)
class ExternalCall:
    # Opaque authenticated transport/session context supplied by the host.
    admission_ref: str
    claimed_tenant: str
    claimed_system: str
    profile_id: str
    payload: dict

class ExternalIdentityProvider(Protocol):
    def verify(self,call:ExternalCall)->VerifiedPrincipal: ...

class SourceOwnershipVerifier(Protocol):
    def verify(self,call:ExternalCall,principal:VerifiedPrincipal)->bool: ...

@dataclass(frozen=True)
class MappingResult:
    output: dict
    mapping_profile: str
    policy_decision_id: str
    intent_sha256: str

def _conservative_item_count(value:Any)->int:
    """Count nested list items conservatively for `max_rows`; cap by policy limit."""
    if isinstance(value,list):
        return len(value)+sum(_conservative_item_count(v) for v in value)
    if isinstance(value,dict):
        return sum(_conservative_item_count(v) for v in value.values())
    return 0

class ExternalMappingBoundary:
    MAX_INPUT_BYTES=512*1024
    def __init__(self,authenticator:ExternalIdentityProvider|None=None,
                 source_verifier:SourceOwnershipVerifier|None=None,
                 policy:PolicyAuthority|None=None,audit:AuditSink|None=None,
                 allowed_profiles:Mapping[str,Path]|None=None):
        self.authenticator=authenticator
        self.source_verifier=source_verifier
        self.security=SecurityGate(policy,audit)
        # Only operator-configured local profiles; callers cannot pick filesystem paths.
        self.allowed_profiles={k:Path(v).resolve() for k,v in (allowed_profiles or {}).items()}

    def map(self,call:ExternalCall)->MappingResult:
        if self.authenticator is None or self.source_verifier is None:
            raise AdmissionError('AUTHENTICATION_UNCONFIGURED','Host identity and source verification required')
        if not isinstance(call,ExternalCall) or not isinstance(call.payload,dict):
            raise AdmissionError('INPUT_INVALID','Structured input required')
        try: serialized=json.dumps(call.payload,separators=(',',':'),ensure_ascii=False,allow_nan=False)
        except (ValueError,TypeError,RecursionError) as exc:
            raise AdmissionError('INPUT_INVALID','Input must be JSON-safe') from exc
        if len(serialized.encode('utf-8'))>self.MAX_INPUT_BYTES:
            raise AdmissionError('INPUT_TOO_LARGE','Mapping input exceeds limit')
        principal=self.authenticator.verify(call)
        if not isinstance(principal,VerifiedPrincipal) or not principal.trusted or principal.audience!='daat':
            raise AdmissionError('AUTHENTICATION_FAILED','Untrusted caller')
        if principal.system!=call.claimed_system or principal.tenant!=call.claimed_tenant:
            raise AdmissionError('AUTHORIZATION_DENIED','Authenticated caller mismatch')
        if not principal.actor:
            raise AdmissionError('ACTOR_UNVERIFIED','Verified actor required for policy evaluation')
        if 'daat-map' not in principal.capabilities:
            raise AdmissionError('AUTHORIZATION_DENIED','Missing mapping capability')
        if not self.source_verifier.verify(call,principal):
            raise AdmissionError('SOURCE_UNTRUSTED','External source provenance unverified')
        if call.profile_id not in self.allowed_profiles:
            raise AdmissionError('MAPPING_PROFILE_DENIED','Profile not configured for this boundary')
        profile,source_schema,target_schema=load_profile(self.allowed_profiles[call.profile_id])
        if call.profile_id != profile['id']+'/'+profile['version']:
            raise AdmissionError('MAPPING_PROFILE_DENIED','Approved profile does not match its declared identity')
        digest=json_digest({'source_digest':json_digest(call.payload),'mapping':profile['id']+'/'+profile['version'],
                            'source_contract':profile['source_contract']['sha256'],
                            'target_contract':profile['target_contract']['sha256']})
        req=PolicyRequest(tenant=principal.tenant,caller=principal.system,
                          actor=principal.actor,action='daat.mapping.execute',
                          resource_owner='daat',resource_class='mapping_profile',
                          resource_selector=profile['id']+'/'+profile['version'],
                          intent_digest=digest,purpose='external_mapping',
                          requested_count=max(1,_conservative_item_count(call.payload)),
                          auth_assurance=principal.auth_assurance,
                          auth_age_seconds=principal.auth_age_seconds)
        decision=self.security.authorize(req)
        output=apply(profile,source_schema,target_schema,call.payload)
        self.security.emit('mapped',decision,req,'success')
        return MappingResult(output,profile['id']+'/'+profile['version'],decision.decision_id,digest)
