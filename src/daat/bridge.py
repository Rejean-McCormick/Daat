"""Injected IK v6 build boundary, offline library only. No transport or public auth server."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime,timezone
import uuid
from typing import Any,Mapping,Protocol
from .contracts import validate_owner,verify_payload_profile
from .errors import AdmissionError,ContractError,MappingError
from .mapping import apply,load_profile
from .util import json_digest
from .security import SecurityGate,PolicyRequest,PolicyAuthority,AuditSink

class Authenticator(Protocol):
    """Host-provided verifier MUST authenticate cryptographic identity; never trust envelope claims."""
    def verify(self,envelope:Mapping[str,Any])->'VerifiedPrincipal': ...

@dataclass(frozen=True)
class VerifiedPrincipal:
    system:str
    tenant:str
    capabilities:frozenset[str]
    trusted:bool
    audience:str='daat'
    actor:str|None=None
    auth_assurance:str='unknown'
    auth_age_seconds:int|None=None

class ArtifactVerifier(Protocol):
    """Owner-provided verifier must validate bytes, digest, and locator authorizations."""
    def verify(self,ref:Mapping[str,Any], principal:VerifiedPrincipal)->bool: ...

class ManifestVerifier(Protocol):
    """Owner-provided verifier checks manifest's producer/owner digest and authority."""
    def verify(self,manifest:Mapping[str,Any], principal:VerifiedPrincipal)->bool: ...

class KristalNativeClient(Protocol):
    def compile(self,structured_input:Mapping[str,Any],*,requested_outputs:list[str])->list[Mapping[str,Any]]: ...

@dataclass(frozen=True)
class Outcome:
    acceptance:dict
    final:dict
    event:dict
    artifact_refs:tuple[dict,...]

class MemoryJournal:
    """Test-only in-memory replay cache. Not a durable exactly-once transaction system."""
    def __init__(self): self._items:dict[tuple,tuple[str,Outcome|None]]={}
    def lookup(self,key:tuple,digest:str)->Outcome|None:
        if key in self._items:
            old,val=self._items[key]
            if old!=digest: raise AdmissionError('IDEMPOTENCY_CONFLICT','Key replay with different request')
            if val is None: raise AdmissionError('IN_PROGRESS','Incomplete previous operation requires owner reconciliation')
            return deepcopy(val)
        return None
    def begin(self,key:tuple,digest:str)->None: self._items[key]=(digest,None)
    def success(self,key:tuple,digest:str,outcome:Outcome)->None: self._items[key]=(digest,deepcopy(outcome))


def _stamp()->str:
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

def receipt(envelope:Mapping[str,Any],status:str,code:str|None=None)->dict:
    item={'specversion':'ik/1.1','record_type':'receipt','id':'receipt-'+str(uuid.uuid4()),
          'time':_stamp(),'interaction_id':envelope['id'],'source':{'system':'daat'},
          'status':status,'retryable':False,'data':{}}
    if code: item['code']=code
    if envelope.get('correlation_id'): item['correlation_id']=envelope['correlation_id']
    validate_owner('receipt',item)
    return item

def validate_ref(ref:Mapping[str,Any])->None:
    validate_owner('artifact-ref',ref)
    loc=(ref.get('locator') or {}).get('ref')
    # No fetching: only opaque URNs in this local boundary. Real transport is IK-owner work.
    if loc is not None and (not loc.startswith('urn:') or '\\' in loc or any(ord(c)<32 for c in loc)):
        raise AdmissionError('LOCATOR_UNTRUSTED','Only opaque urn: references admitted offline')
    if not ref.get('integrity'):
        raise AdmissionError('ARTIFACT_INTEGRITY_FAILURE','Artifact requires declared integrity')

class V6BuildBridge:
    """Admits only existing owner-approved IK command/profile and invokes injected native port."""
    def __init__(self,authenticator:Authenticator|None=None, artifact_verifier:ArtifactVerifier|None=None,
                 manifest_verifier:ManifestVerifier|None=None,journal:MemoryJournal|None=None,
                 policy:PolicyAuthority|None=None,audit:AuditSink|None=None):
        self.authenticator=authenticator
        self.artifact_verifier=artifact_verifier
        self.manifest_verifier=manifest_verifier
        self.journal=journal or MemoryJournal()
        self.security=SecurityGate(policy,audit)

    def process(self,envelope:dict,manifest:dict,profile_path,client:KristalNativeClient)->Outcome:
        # No mock fallback or implicit trust if a verifier was not injected.
        if any(x is None for x in (self.authenticator,self.artifact_verifier,self.manifest_verifier)):
            raise AdmissionError('AUTHENTICATION_UNCONFIGURED','Trusted providers required; no server default')
        verify_payload_profile(envelope)
        validate_owner('export-manifest',manifest)
        principal=self.authenticator.verify(envelope)
        if not isinstance(principal,VerifiedPrincipal) or not principal.trusted or principal.audience!='daat':
            raise AdmissionError('AUTHENTICATION_FAILED','Untrusted principal')
        if principal.system!=envelope['source']['system'] or principal.tenant!=envelope['source'].get('organization'):
            raise AdmissionError('AUTHORIZATION_DENIED','Principal/source/tenant mismatch')
        # An authenticated workload is not a verified actor assertion.
        # The host must supply an independently verified human or service-principal actor.
        if not principal.actor:
            raise AdmissionError('ACTOR_UNVERIFIED','Verified actor required for policy evaluation')
        if 'kristal-build' not in principal.capabilities:
            raise AdmissionError('AUTHORIZATION_DENIED','Missing build capability')
        if manifest['producer'].get('system')!=principal.system or manifest['producer'].get('organization')!=principal.tenant:
            raise AdmissionError('AUTHORIZATION_DENIED','Manifest producer not authorized')
        if not self.manifest_verifier.verify(manifest,principal):
            raise AdmissionError('ARTIFACT_INTEGRITY_FAILURE','Owner manifest integrity not verified')
        for ref in envelope['artifact_refs']:
            validate_ref(ref)
            if ref['owner'].get('system')!=principal.system or ref['owner'].get('organization')!=principal.tenant:
                raise AdmissionError('AUTHORIZATION_DENIED','Foreign artifact not authorized')
            if not self.artifact_verifier.verify(ref,principal):
                raise AdmissionError('ARTIFACT_INTEGRITY_FAILURE','Source artifact not verified')
        profile,source_schema,target_schema=load_profile(profile_path)
        if envelope['data']['mapping_profile']!=profile['id']+'/'+profile['version']:
            raise ContractError('MAPPING_PROFILE_MISMATCH','Envelope and selected mapping disagree')
        key=(principal.system,principal.tenant,'kristal.build.request/2.0.0',envelope['idempotency_key'])
        digest=json_digest({'envelope':envelope,'manifest':manifest,'mapping_profile':profile['id']+'/'+profile['version'],
                            'source_pin':profile['source_contract']['sha256'],'target_pin':profile['target_contract']['sha256']})
        # Owner-policy decision is bound to precise request, tenant, resource, profile and digest.
        # It is re-evaluated on each replay: a revoked caller cannot use a cached success.
        policy_request=PolicyRequest(tenant=principal.tenant,caller=principal.system,
            actor=principal.actor,action='kristal.build.request',
            resource_owner='kristal',resource_class='kristal_build',
            resource_selector=envelope['id'],intent_digest=digest,
            requested_count=len(envelope['artifact_refs']),purpose='kristal_build',
            auth_assurance=principal.auth_assurance,auth_age_seconds=principal.auth_age_seconds)
        policy_decision=self.security.authorize(policy_request)
        previous=self.journal.lookup(key,digest)
        if previous is not None:
            self.security.emit('replay',policy_decision,policy_request,'cached_success')
            return previous
        structured=apply(profile,source_schema,target_schema,manifest)
        self.journal.begin(key,digest)
        # Record authorization before native side effects; if audit fails this is left
        # in-doubt, not retried automatically (reconciliation required).
        self.security.emit('started',policy_decision,policy_request,'in_progress')
        accepted=receipt(envelope,'accepted')
        try:
            artifacts=client.compile(structured,requested_outputs=list(envelope['data']['requested_outputs']))
            if not isinstance(artifacts,list) or not artifacts:
                raise ContractError('OUTPUT_INVALID','Native client returned no artifacts')
            for ref in artifacts:
                validate_ref(ref)
                if ref['owner'].get('system')!='kristal' or ref['owner'].get('organization')!=principal.tenant:
                    raise AdmissionError('AUTHORIZATION_DENIED','Native output owner/tenant mismatch')
                if not self.artifact_verifier.verify(ref,principal):
                    raise AdmissionError('ARTIFACT_INTEGRITY_FAILURE','Native artifact not verified')
            final=receipt(envelope,'succeeded')
            event={'specversion':'ik/1.1','id':'event-'+str(uuid.uuid4()),'class':'event','time':_stamp(),
                'profile':{'id':'kristal.artifact.ready','version':'2.0.0'},
                'source':{'system':'daat'},'subject':envelope['subject'],
                'data':{'build_ref':envelope['id'],'stage':'kristal-state'},
                'artifact_refs':deepcopy(artifacts)}
            if envelope.get('correlation_id'): event['correlation_id']=envelope['correlation_id']
            validate_owner('envelope',event)
            validate_owner('ready',event['data'])
            outcome=Outcome(accepted,final,event,tuple(deepcopy(artifacts)))
            # Do not report success until local audit commitment has succeeded.
            self.security.emit('completed',policy_decision,policy_request,'success')
            self.journal.success(key,digest,outcome)
            return outcome
        except Exception:
            # Intentional retained in-progress journal: native side-effect may have happened.
            # Owner reconciliation required before any retry.
            raise
