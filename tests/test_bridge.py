from dataclasses import replace
import copy
import pytest
from daat.bridge import V6BuildBridge,VerifiedPrincipal,validate_ref,receipt
from daat.contracts import validate_owner
from daat.errors import AdmissionError,ContractError,MappingError
from daat.util import load_json
from test_contracts import build_envelope,ref
from security_fixtures import SyntheticPolicy,SyntheticAudit

class FakeAuth:
    def __init__(self,principal=None):
        self.principal=principal or VerifiedPrincipal('orgo','school-demo',frozenset({'kristal-build'}),True,actor='svc:orgo')
        if self.principal.actor is None and self.principal.trusted:
            self.principal=replace(self.principal,actor='svc:orgo')
    def verify(self,e): return self.principal

class FakeArtifactVerifier:
    def __init__(self,passes=True): self.passes=passes
    def verify(self,r,p): return self.passes

class FakeManifestVerifier:
    def __init__(self,passes=True):self.passes=passes
    def verify(self,m,p):return self.passes

class FakeKristal:
    def __init__(self):self.calls=0;self.result=[ref(owner='kristal',tenant='school-demo')]
    def compile(self,structured_input,*,requested_outputs):
        self.calls+=1
        assert requested_outputs==['kristal_state']
        assert structured_input['producer']['system']=='orgo'
        return copy.deepcopy(self.result)

@pytest.fixture
def manifest(native_profile): return load_json(native_profile.parent/'examples/golden.input.json')

@pytest.fixture
def bridge(): return V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit())

def test_no_trust_default_fails(manifest,native_profile):
    with pytest.raises(AdmissionError) as e:V6BuildBridge().process(build_envelope(),manifest,native_profile,FakeKristal())
    assert e.value.code=='AUTHENTICATION_UNCONFIGURED'

def test_synthetic_authorized_bridge(bridge,native_profile,manifest):
    envelope=build_envelope();fake=FakeKristal()
    out=bridge.process(envelope,manifest,native_profile,fake)
    assert fake.calls==1
    assert out.acceptance['status']=='accepted'
    assert out.final['status']=='succeeded'
    assert out.event['data']['stage']=='kristal-state'
    assert out.event['artifact_refs'][0]['owner']['system']=='kristal'
    validate_owner('receipt',out.final);validate_owner('envelope',out.event)

def test_replay_no_duplicate_native(bridge,native_profile,manifest):
    fake=FakeKristal();e=build_envelope()
    a=bridge.process(e,manifest,native_profile,fake)
    b=bridge.process(e,manifest,native_profile,fake)
    assert a==b and fake.calls==1

def test_replay_conflict(bridge,native_profile,manifest):
    fake=FakeKristal(); e=build_envelope()
    bridge.process(e,manifest,native_profile,fake)
    mutated=copy.deepcopy(manifest);mutated['id']='altered'
    with pytest.raises(AdmissionError) as ex:bridge.process(e,mutated,native_profile,fake)
    assert ex.value.code=='IDEMPOTENCY_CONFLICT' and fake.calls==1

def test_expired_or_untrusted_principal(native_profile,manifest):
    bridge=V6BuildBridge(FakeAuth(VerifiedPrincipal('orgo','school-demo',frozenset({'kristal-build'}),False)),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit())
    with pytest.raises(AdmissionError):bridge.process(build_envelope(),manifest,native_profile,FakeKristal())

def test_cross_tenant(native_profile,manifest):
    bridge=V6BuildBridge(FakeAuth(VerifiedPrincipal('orgo','other-tenant',frozenset({'kristal-build'}),True)),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit())
    with pytest.raises(AdmissionError) as e:bridge.process(build_envelope(),manifest,native_profile,FakeKristal())
    assert e.value.code=='AUTHORIZATION_DENIED'

def test_missing_capability(native_profile,manifest):
    bridge=V6BuildBridge(FakeAuth(VerifiedPrincipal('orgo','school-demo',frozenset(),True)),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit())
    with pytest.raises(AdmissionError):bridge.process(build_envelope(),manifest,native_profile,FakeKristal())

def test_forged_manifest_rejected(bridge,native_profile,manifest):
    manifest['producer']['organization']='someone-else'
    with pytest.raises(AdmissionError):bridge.process(build_envelope(),manifest,native_profile,FakeKristal())

def test_unverified_manifest_rejected(native_profile,manifest):
    bridge=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(False),policy=SyntheticPolicy(),audit=SyntheticAudit())
    with pytest.raises(AdmissionError):bridge.process(build_envelope(),manifest,native_profile,FakeKristal())

def test_unverified_source_ref_rejected(native_profile,manifest):
    bridge=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(False),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit())
    with pytest.raises(AdmissionError):bridge.process(build_envelope(),manifest,native_profile,FakeKristal())

def test_malicious_locator(bridge,native_profile,manifest):
    e=build_envelope();e['artifact_refs'][0]['locator']['ref']='http://169.254.169.254/latest/meta-data'
    with pytest.raises(AdmissionError) as x:bridge.process(e,manifest,native_profile,FakeKristal())
    assert x.value.code=='LOCATOR_UNTRUSTED'

def test_secret_in_locator_rejected(bridge,native_profile,manifest):
    e=build_envelope();e['artifact_refs'][0]['locator']['ref']='https://u:p@foo.example/file'
    with pytest.raises(ContractError):bridge.process(e,manifest,native_profile,FakeKristal())

def test_native_failure_stays_in_progress(bridge,native_profile,manifest):
    class Failed(FakeKristal):
        def compile(self,*args,**kwargs):
            self.calls+=1
            raise RuntimeError('simulated crash after unknown side effect')
    failed=Failed();e=build_envelope()
    with pytest.raises(RuntimeError):bridge.process(e,manifest,native_profile,failed)
    with pytest.raises(AdmissionError) as x:bridge.process(e,manifest,native_profile,FakeKristal())
    assert x.value.code=='IN_PROGRESS'

def test_invalid_native_output_never_success(bridge,native_profile,manifest):
    fake=FakeKristal();fake.result=[{'owner':{'system':'kristal'},'artifact_type':'state','artifact_id':'x'}]
    with pytest.raises(AdmissionError):bridge.process(build_envelope(),manifest,native_profile,fake)

def test_mapping_identity_not_owner_authority(bridge,native_profile,manifest):
    out=bridge.process(build_envelope(),manifest,native_profile,FakeKristal())
    assert out.event['artifact_refs'][0]['owner']['system']=='kristal'
    assert out.event['source']['system']=='daat'

def test_unapproved_build_profile(bridge,native_profile,manifest):
    e=build_envelope();e['data']['mapping_profile']='outside-inventory/1.0.0'
    with pytest.raises(ContractError) as ex:bridge.process(e,manifest,native_profile,FakeKristal())
    assert ex.value.code=='MAPPING_PROFILE_MISMATCH'

def test_replay_reauthorized_after_policy_revoke(native_profile,manifest):
    policy=SyntheticPolicy(); audit=SyntheticAudit()
    bridge=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),policy=policy,audit=audit)
    fake=FakeKristal();envelope=build_envelope()
    bridge.process(envelope,manifest,native_profile,fake)
    policy.decision='DENY'
    with pytest.raises(AdmissionError) as e:bridge.process(envelope,manifest,native_profile,fake)
    assert e.value.code=='POLICY_DENIED' and fake.calls==1

def test_missing_actor_refused(native_profile,manifest):
    class RawAuth:
        def verify(self,envelope):
            return VerifiedPrincipal('orgo','school-demo',frozenset({'kristal-build'}),True)
    b=V6BuildBridge(RawAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit())
    with pytest.raises(AdmissionError) as e:b.process(build_envelope(),manifest,native_profile,FakeKristal())
    assert e.value.code=='ACTOR_UNVERIFIED'

def test_native_output_cross_tenant_rejected(bridge,native_profile,manifest):
    fake=FakeKristal();fake.result=[ref(owner='kristal',tenant='another-school')]
    with pytest.raises(AdmissionError) as e:bridge.process(build_envelope(),manifest,native_profile,fake)
    assert e.value.code=='AUTHORIZATION_DENIED'

def test_audit_failure_before_effect_blocks_native(native_profile,manifest):
    b=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=SyntheticAudit(broken=True))
    client=FakeKristal()
    with pytest.raises(AdmissionError) as e:b.process(build_envelope(),manifest,native_profile,client)
    assert e.value.code=='AUDIT_UNAVAILABLE' and client.calls==0

def test_audit_failure_after_effect_requires_reconciliation(native_profile,manifest):
    class ThirdRecordFails(SyntheticAudit):
        def record(self,record):
            if record.stage=='completed':raise OSError('audit sink unavailable')
            super().record(record)
    audit=ThirdRecordFails()
    b=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy(),audit=audit)
    client=FakeKristal(); envelope=build_envelope()
    with pytest.raises(AdmissionError) as e:b.process(envelope,manifest,native_profile,client)
    assert e.value.code=='AUDIT_UNAVAILABLE' and client.calls==1
    with pytest.raises(AdmissionError) as e:b.process(envelope,manifest,native_profile,client)
    assert e.value.code=='IN_PROGRESS' and client.calls==1


def test_policy_missing_is_fail_closed_before_build(native_profile,manifest):
    b=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),audit=SyntheticAudit())
    native=FakeKristal()
    with pytest.raises(AdmissionError) as e:b.process(build_envelope(),manifest,native_profile,native)
    assert e.value.code=='SECURITY_UNCONFIGURED' and native.calls==0

def test_audit_missing_is_fail_closed_before_build(native_profile,manifest):
    b=V6BuildBridge(FakeAuth(),FakeArtifactVerifier(),FakeManifestVerifier(),policy=SyntheticPolicy())
    native=FakeKristal()
    with pytest.raises(AdmissionError) as e:b.process(build_envelope(),manifest,native_profile,native)
    assert e.value.code=='SECURITY_UNCONFIGURED' and native.calls==0
