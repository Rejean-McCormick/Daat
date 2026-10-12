import copy
import json
from pathlib import Path
import pytest
from daat.contracts import verify_baseline,validate_owner,verify_payload_profile,OWNERS
from daat.errors import ContractError

GOOD_DIGEST='sha256:'+'a'*64

def ref(owner='orgo',tenant='school-demo'):
    return {'owner':{'system':owner,'organization':tenant},'artifact_type':'test.export',
            'artifact_id':'sample-1','integrity':{'algorithm':'sha256','digest':GOOD_DIGEST},
            'locator':{'ref':'urn:sample:export:1'}}

def build_envelope():
    return {
        'specversion':'ik/1.1','id':'request-test-1234','class':'command','time':'2026-10-12T12:00:00Z',
        'profile':{'id':'kristal.build.request','version':'2.0.0'},
        'source':{'system':'orgo','organization':'school-demo'},'target':{'system':'daat'},
        'subject':{'type':'project','id':'scene-1'},'authority':{'kind':'operational-workflow'},
        'idempotency_key':'req-unique-01',
        'artifact_refs':[ref()],
        'response':{'acceptance_receipt':True,'final_receipt':True,'outcome_events':['kristal.artifact.ready']},
        'data':{'mapping_profile':'native-export-identity/1.0.0',
                'requested_outputs':['kristal_state'],'kristal_contract_set':'6.0.0'}
    }

def test_pins_ok(): assert verify_baseline()['files']>=8

def test_owner_schemas():
    validate_owner('envelope',build_envelope());validate_owner('artifact-ref',ref())

def test_unknown_properties_rejected():
    v=build_envelope();v['danger']='hello'
    with pytest.raises(ContractError,match='invalid'):validate_owner('envelope',v)

def test_bad_date_rejected():
    v=build_envelope();v['time']='yesterday'
    with pytest.raises(ContractError):validate_owner('envelope',v)

def test_wrong_target():
    v=build_envelope();v['target']['system']='not-daat'
    with pytest.raises(ContractError) as e:verify_payload_profile(v)
    assert e.value.code=='TARGET_MISMATCH'

def test_wrong_contract():
    v=build_envelope();v['data']['kristal_contract_set']='7.0.0'
    with pytest.raises(ContractError) as e:verify_payload_profile(v)
    assert e.value.code=='SCHEMA_INVALID'

def test_wrong_profile():
    v=build_envelope();v['profile']['version']='99.0.0'
    with pytest.raises(ContractError) as e:verify_payload_profile(v)
    assert e.value.code=='UNKNOWN_PROFILE'

def test_no_idempotency():
    v=build_envelope();v.pop('idempotency_key')
    with pytest.raises(ContractError) as e:verify_payload_profile(v)
    assert e.value.code=='MISSING_EXPORT'

def test_authority_required():
    v=build_envelope();v.pop('authority')
    with pytest.raises(ContractError):verify_payload_profile(v)

def test_unknown_source():
    v=build_envelope();v['source']['system']='outside'
    with pytest.raises(ContractError) as e:verify_payload_profile(v)
    assert e.value.code=='UNAUTHORIZED_SOURCE_PROFILE'

def test_pin_tamper(tmp_path):
    import shutil
    root=tmp_path/'ik';shutil.copytree(OWNERS,root)
    p=root/'envelope.schema.json';p.write_text(p.read_text()+'\n')
    with pytest.raises(ContractError) as e:verify_baseline(root)
    assert e.value.code=='CONTRACT_PIN_MISMATCH'

def test_new_owner_schema_does_not_sneak_in(tmp_path):
    import shutil
    root=tmp_path/'ik';shutil.copytree(OWNERS,root)
    (root/'new.schema.json').write_text('{}')
    with pytest.raises(ContractError):verify_baseline(root)

def test_authority_null_rejected():
    e=build_envelope();e['authority']=None
    with pytest.raises(ContractError):verify_payload_profile(e)

def test_only_supported_ready_stage_requested():
    e=build_envelope();e['data']['requested_outputs']=['validation_report']
    with pytest.raises(ContractError) as x:verify_payload_profile(e)
    assert x.value.code=='UNSUPPORTED_OUTPUT'
