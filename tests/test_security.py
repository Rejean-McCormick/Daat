from dataclasses import replace
from datetime import datetime,timedelta,timezone
from pathlib import Path
import pytest
from daat.errors import AdmissionError
from daat.security import SecurityGate,PolicyRequest,BoundDecision
from daat.konfid_port import KonfidPolicyPort
from daat.external import ExternalMappingBoundary,ExternalCall
from daat.bridge import VerifiedPrincipal
from daat.util import json_digest,load_json
from security_fixtures import SyntheticPolicy,SyntheticAudit

def req(**kwargs):
    base=PolicyRequest(tenant='school-demo',caller='orgo',actor='orgo',action='kristal.build.request',
        resource_owner='kristal',resource_class='kristal_build',resource_selector='build:one',
        intent_digest='f'*64)
    return replace(base,**kwargs)

def test_konfid_request_exact_structure_and_identity_binding():
    payload=req().konfid_request()
    assert sorted(payload)==['action','actor','context','request_id','resource','scope','tenant']
    assert payload['resource']['owner']=='kristal'
    assert payload['scope']['caller_service']=='orgo'
    assert req(actor='other').binding!=req().binding
    assert req(tenant='other').binding!=req().binding
    assert req(intent_digest='e'*64).binding!=req().binding
    assert req(resource_selector='other').binding!=req().binding

@pytest.mark.parametrize('invalid',[
    {'tenant':'?bad'},{'actor':''},{'intent_digest':'not-sha'},{'requested_count':0},
    {'requested_count':True},{'resource_selector':''},{'auth_age_seconds':-1}
])
def test_invalid_policy_requests(invalid):
    with pytest.raises(AdmissionError):req(**invalid)

def test_gate_missing_dependencies():
    with pytest.raises(AdmissionError) as error:SecurityGate().authorize(req())
    assert error.value.code=='SECURITY_UNCONFIGURED'

def test_gate_allows_bounded_decision_and_safe_audit():
    audit=SyntheticAudit(); gate=SecurityGate(SyntheticPolicy(),audit)
    gate.authorize(req())
    assert len(audit.items)==1
    assert audit.items[0].request_binding==req().binding
    assert not hasattr(audit.items[0],'raw_payload')

@pytest.mark.parametrize('policy,expected',[
    (SyntheticPolicy(tamper=True),'POLICY_BINDING_MISMATCH'),
    (SyntheticPolicy(decision='DENY'),'POLICY_DENIED'),
    (SyntheticPolicy(decision='BLOCKED'),'POLICY_DENIED'),
    (SyntheticPolicy(decision='STEP_UP_REQUIRED'),'POLICY_DENIED'),
    (SyntheticPolicy(decision='APPROVAL_REQUIRED'),'POLICY_DENIED'),
    (SyntheticPolicy(expire_seconds=-2),'POLICY_EXPIRED'),
    (SyntheticPolicy(expire_seconds=500),'POLICY_EXPIRED'),
    (SyntheticPolicy(obligations=({'type':'unknown'},)),'POLICY_OBLIGATION_UNKNOWN'),
    (SyntheticPolicy(obligations=({'type':'no_export'},)),'POLICY_OBLIGATION_DENIED'),
    (SyntheticPolicy(obligations=({'type':'max_rows','value':0},)),'POLICY_OBLIGATION_DENIED'),
    (SyntheticPolicy(obligations=({'type':'audit','level':'magic'},)),'POLICY_OBLIGATION_UNKNOWN'),
])
def test_policy_negative_paths(policy,expected):
    with pytest.raises(AdmissionError) as error:SecurityGate(policy,SyntheticAudit()).authorize(req())
    assert error.value.code==expected

def test_policy_supported_obligations():
    policy=SyntheticPolicy(obligations=({'type':'max_rows','value':5}, {'type':'audit','level':'standard'},
                                        {'type':'authority_source','value':'grant:demo'}))
    assert SecurityGate(policy,SyntheticAudit()).authorize(req()).decision=='ALLOW'

def test_bad_policy_provider_fails_closed():
    class Offline:
        def evaluate(self,_):raise ConnectionError('secret-url=internal')
    with pytest.raises(AdmissionError) as error:SecurityGate(Offline(),SyntheticAudit()).authorize(req())
    assert error.value.code=='POLICY_UNAVAILABLE'
    assert 'secret-url' not in str(error.value)

def test_unavailable_audit_fails_closed():
    with pytest.raises(AdmissionError) as error:SecurityGate(SyntheticPolicy(),SyntheticAudit(broken=True)).authorize(req())
    assert error.value.code=='AUDIT_UNAVAILABLE'

def test_konfid_response_converted_only_from_trusted_port():
    seen=[]
    def trusted_rpc(data):
        seen.append(data)
        return {'decision_id':'PD-known','decision':'ALLOW','policy':'koa/policy-1',
                'valid_until':(datetime.now(timezone.utc)+timedelta(seconds=25)).isoformat(),
                'obligations':[{'type':'max_rows','value':2}]}
    policy=KonfidPolicyPort(trusted_rpc)
    SecurityGate(policy,SyntheticAudit()).authorize(req())
    assert seen[0]['context']['purpose']=='integration'

def test_konfid_no_expiry_does_not_grant_authority():
    policy=KonfidPolicyPort(lambda x:{'decision_id':'PD','decision':'ALLOW','policy':'koa/v1',
                                      'valid_until':None,'obligations':[]})
    with pytest.raises(AdmissionError) as e:SecurityGate(policy,SyntheticAudit()).authorize(req())
    assert e.value.code=='POLICY_EXPIRED'

class FakeExternalAuth:
    def __init__(self,tenant='school-demo',caps=None):self.tenant=tenant;self.caps=caps or frozenset({'daat-map'})
    def verify(self,call):return VerifiedPrincipal('outside-app',self.tenant,self.caps,True,actor='svc:outside-app')
class VerifiedSource:
    def __init__(self,good=True):self.good=good
    def verify(self,call,principal):return self.good

@pytest.fixture
def external_call():
    root=Path(__file__).resolve().parents[1]/'mappings/foreign-inventory'
    return ExternalCall(admission_ref='host-attested-001',claimed_system='outside-app',claimed_tenant='school-demo',
                        profile_id='outside-inventory/1.0.0',payload=load_json(root/'examples/golden.input.json'))

@pytest.fixture
def allowed_profiles():
    root=Path(__file__).resolve().parents[1]/'mappings'
    return {'outside-inventory/1.0.0':root/'foreign-inventory/profile.json',
            'native-export-identity/1.0.0':root/'native/profile.json'}

def external_boundary(allowed_profiles,**kw):
    args=dict(authenticator=FakeExternalAuth(),source_verifier=VerifiedSource(),
              policy=SyntheticPolicy(),audit=SyntheticAudit(),allowed_profiles=allowed_profiles)
    args.update(kw)
    return ExternalMappingBoundary(**args)

def test_external_mapping_through_security_gate(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles)
    result=gate.map(external_call)
    expected=load_json(Path(__file__).resolve().parents[1]/'mappings/foreign-inventory/examples/golden.expected.json')
    assert result.output==expected
    assert result.mapping_profile==external_call.profile_id

def test_external_unconfigured_identity_fails(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles,authenticator=None)
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='AUTHENTICATION_UNCONFIGURED'

def test_external_identity_tenant_mismatch_fails(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles,authenticator=FakeExternalAuth(tenant='untrusted-tenant'))
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='AUTHORIZATION_DENIED'

def test_external_unverified_source_fails(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles,source_verifier=VerifiedSource(False))
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='SOURCE_UNTRUSTED'

def test_external_unapproved_profile_fails(external_call,allowed_profiles):
    gate=external_boundary({})
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='MAPPING_PROFILE_DENIED'

def test_external_policy_denied(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles,policy=SyntheticPolicy(decision='DENY'))
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='POLICY_DENIED'

def test_external_large_input_rejected(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles)
    with pytest.raises(AdmissionError) as e:gate.map(replace(external_call,payload={'x':'A'*600000}))
    assert e.value.code=='INPUT_TOO_LARGE'

def test_external_not_allowed_to_use_arbitrary_profile_path(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles)
    with pytest.raises(AdmissionError) as e:gate.map(replace(external_call,profile_id='/etc/passwd'))
    assert e.value.code=='MAPPING_PROFILE_DENIED'

def test_external_capability_absent(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles,authenticator=FakeExternalAuth(caps=frozenset({'different'})))
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='AUTHORIZATION_DENIED'

def test_external_unverified_actor_rejected(external_call,allowed_profiles):
    class MissingActor:
        def verify(self,call):return VerifiedPrincipal('outside-app','school-demo',frozenset({'daat-map'}),True)
    gate=external_boundary(allowed_profiles,authenticator=MissingActor())
    with pytest.raises(AdmissionError) as e:gate.map(external_call)
    assert e.value.code=='ACTOR_UNVERIFIED'

def test_external_native_zero_transform_still_requires_security(allowed_profiles):
    root=Path(__file__).resolve().parents[1]/'mappings/native'
    call=ExternalCall('synthetic', 'school-demo','outside-app','native-export-identity/1.0.0',
                      load_json(root/'examples/golden.input.json'))
    gate=external_boundary(allowed_profiles,policy=SyntheticPolicy(decision='DENY'))
    with pytest.raises(AdmissionError) as e:gate.map(call)
    assert e.value.code=='POLICY_DENIED'


def test_external_policy_row_limit_counts_nested_collection(external_call,allowed_profiles):
    gate=external_boundary(allowed_profiles,policy=SyntheticPolicy(obligations=({'type':'max_rows','value':1},)))
    payload=dict(external_call.payload)
    payload['items']=[{'id':1},{'id':2}]
    with pytest.raises(AdmissionError) as e:gate.map(replace(external_call,payload=payload))
    assert e.value.code=='POLICY_OBLIGATION_DENIED'
