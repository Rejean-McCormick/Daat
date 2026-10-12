"""Owner-admitted security enforcement at the DaaT boundary.

No identity provider, policy server, credentials, or HTTP client is implemented here.
The host must validate workload identity and optional human actor assertion, and
ask Konfid/kOA for each authorization. DaaT then enforces a *bound*, short-lived
response and the supported obligations. Unknown obligations fail closed.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Protocol, Any, Mapping
import re
from .errors import AdmissionError
from .util import json_digest

_MAX_POLICY_TTL = timedelta(seconds=120)
_SAFE_IDENTIFIER = re.compile(r'^[a-zA-Z0-9_.:/-]{2,128}$')

@dataclass(frozen=True)
class PolicyRequest:
    tenant: str
    caller: str
    actor: str
    action: str
    resource_owner: str
    resource_class: str
    resource_selector: str
    intent_digest: str
    requested_count: int = 1
    purpose: str = 'integration'
    auth_assurance: str = 'unknown'
    auth_age_seconds: int | None = None

    def __post_init__(self):
        for name in ('tenant','caller','actor','action','resource_owner','resource_class'):
            value=getattr(self,name)
            if not isinstance(value,str) or not _SAFE_IDENTIFIER.fullmatch(value):
                raise AdmissionError('POLICY_REQUEST_INVALID',f'Invalid policy {name}')
        if not isinstance(self.resource_selector,str) or not self.resource_selector or len(self.resource_selector)>1024:
            raise AdmissionError('POLICY_REQUEST_INVALID','Invalid resource selector')
        if not re.fullmatch('[a-f0-9]{64}',self.intent_digest):
            raise AdmissionError('POLICY_REQUEST_INVALID','Invalid intent digest')
        if not isinstance(self.requested_count,int) or isinstance(self.requested_count,bool) or not (1<=self.requested_count<=10000):
            raise AdmissionError('POLICY_REQUEST_INVALID','Invalid count')
        if self.auth_age_seconds is not None and (type(self.auth_age_seconds) is not int or self.auth_age_seconds<0):
            raise AdmissionError('POLICY_REQUEST_INVALID','Invalid age')

    @property
    def binding(self)->str:
        return json_digest({
            'tenant':self.tenant,'caller':self.caller,'actor':self.actor,
            'action':self.action,'owner':self.resource_owner,'resource_class':self.resource_class,
            'selector':self.resource_selector,'intent':self.intent_digest,
            'requested_count':self.requested_count,'purpose':self.purpose,
            'assurance':self.auth_assurance,'auth_age_seconds':self.auth_age_seconds
        })

    def konfid_request(self)->dict[str,Any]:
        """Exactly Konfid AccessRequest fields, not a new wire protocol."""
        return {
            'request_id':'DAAT-'+self.binding[:48], 'tenant':self.tenant,
            'actor':self.actor, 'action':self.action,
            'resource':{'owner':self.resource_owner,'class':self.resource_class,'selector':self.resource_selector},
            'scope':{'caller_service':self.caller,'intent_sha256':self.intent_digest},
            'context':{'auth_assurance':self.auth_assurance,
                       'auth_age_seconds':self.auth_age_seconds,
                       'requested_count':self.requested_count,
                       'purpose':self.purpose}
        }

@dataclass(frozen=True)
class BoundDecision:
    """Host-bound Konfid AccessResponse. Host must authenticate response provenance."""
    binding: str
    decision: str
    decision_id: str
    policy: str
    valid_until: datetime | None
    obligations: tuple[Mapping[str,Any],...] = field(default_factory=tuple)

class PolicyAuthority(Protocol):
    def evaluate(self, request:PolicyRequest)->BoundDecision: ...

@dataclass(frozen=True)
class AuditRecord:
    # Never contain raw payload, manifest, tokens, source locators or actor PII.
    stage: str
    decision_id: str
    request_binding: str
    outcome: str
    record_type: str = 'daat.security/0.3.0'

class AuditSink(Protocol):
    def record(self,item:AuditRecord)->None: ...

class SecurityGate:
    def __init__(self, policy:PolicyAuthority|None=None, audit:AuditSink|None=None):
        self.policy=policy
        self.audit=audit

    def authorize(self,request:PolicyRequest)->BoundDecision:
        if self.policy is None or self.audit is None:
            raise AdmissionError('SECURITY_UNCONFIGURED','Trusted policy authority and audit sink are required')
        try: decision=self.policy.evaluate(request)
        except Exception as exc:
            raise AdmissionError('POLICY_UNAVAILABLE','Policy decision unavailable') from exc
        if not isinstance(decision,BoundDecision):
            raise AdmissionError('POLICY_INVALID','Policy decision not bound')
        if decision.binding!=request.binding:
            raise AdmissionError('POLICY_BINDING_MISMATCH','Decision does not bind the exact intent')
        if decision.decision not in ('ALLOW','DENY','BLOCKED','STEP_UP_REQUIRED','APPROVAL_REQUIRED'):
            raise AdmissionError('POLICY_INVALID','Unknown policy decision')
        if decision.decision!='ALLOW':
            self.emit('denied',decision,request,'deny')
            raise AdmissionError('POLICY_DENIED','Operation not authorized')
        if not decision.decision_id or not decision.policy or len(decision.decision_id)>128 or len(decision.policy)>128:
            raise AdmissionError('POLICY_INVALID','Missing policy reference')
        now=datetime.now(timezone.utc)
        expiry=decision.valid_until
        if not isinstance(expiry,datetime) or expiry.tzinfo is None or expiry.utcoffset() is None:
            raise AdmissionError('POLICY_EXPIRED','Missing timezone-aware decision expiry')
        if not (now < expiry <= now + _MAX_POLICY_TTL):
            raise AdmissionError('POLICY_EXPIRED','Stale or overlong decision validity')
        if not isinstance(decision.obligations,tuple) or len(decision.obligations)>32:
            raise AdmissionError('POLICY_INVALID','Malformed obligations')
        for ob in decision.obligations:
            if not isinstance(ob,dict) or not isinstance(ob.get('type'),str):
                raise AdmissionError('POLICY_OBLIGATION_UNKNOWN','Invalid obligation')
            typ=ob['type']
            if typ=='max_rows':
                count=ob.get('value')
                if type(count) is not int or count<0 or request.requested_count>count:
                    raise AdmissionError('POLICY_OBLIGATION_DENIED','Row limit exceeded')
            elif typ=='audit':
                if ob.get('level') not in ('basic','standard','enhanced','full'):
                    raise AdmissionError('POLICY_OBLIGATION_UNKNOWN','Unknown audit level')
            elif typ=='authority_source':
                if not isinstance(ob.get('value'),str) or not ob['value'] or len(ob['value'])>256:
                    raise AdmissionError('POLICY_OBLIGATION_UNKNOWN','Invalid authority source')
            elif typ=='no_export':
                raise AdmissionError('POLICY_OBLIGATION_DENIED','Export prohibited')
            else:
                raise AdmissionError('POLICY_OBLIGATION_UNKNOWN','Unsupported policy obligation')
        self.emit('authorized',decision,request,'allow')
        return decision

    def emit(self,stage:str,decision:BoundDecision,request:PolicyRequest,outcome:str)->None:
        if self.audit is None: raise AdmissionError('SECURITY_UNCONFIGURED','Audit sink required')
        item=AuditRecord(stage=stage,decision_id=decision.decision_id,
                         request_binding=request.binding,outcome=outcome)
        try: self.audit.record(item)
        except Exception as exc:
            raise AdmissionError('AUDIT_UNAVAILABLE','Security audit persistence failed') from exc
