import copy
import json
import pytest
from daat.mapping import load_profile,apply,map_file,check_profile
from daat.errors import MappingError
from daat.alignment import evaluate
from daat.util import load_json

@pytest.mark.parametrize('which',['native_profile','foreign_profile'])
def test_golden(which,request):
    path=request.getfixturevalue(which)
    profile,source,target=load_profile(path)
    assert apply(profile,source,target,load_json(path.parent/'examples/golden.input.json'))==load_json(path.parent/'examples/golden.expected.json')

def test_identity_score(native_profile):
    report=evaluate(native_profile)
    assert report['burden_points']==0
    assert report['zero_semantic_transform']
    assert report['coverage']==1 and report['golden_verified']
    assert not report['conformant_for_scope']

def test_foreign_score(foreign_profile):
    r=evaluate(foreign_profile)
    assert r['burden_points']==4
    assert not r['zero_semantic_transform']
    assert r['loss_count']==0

def test_missing_field(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    del item['owner']
    with pytest.raises(MappingError):apply(p,s,t,item)

def test_unknown_enum(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    item['measurement']='km'
    with pytest.raises(MappingError):apply(p,s,t,item)

def test_extra_source_field_is_never_dropped_silently(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    s['properties']['surprise']={'type':'string'}
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    item['surprise']='do-not-drop'
    with pytest.raises(MappingError) as e:apply(p,s,t,item)
    assert e.value.code=='MAPPING_LOSS_FORBIDDEN'

def test_explicit_optional_exclusion(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    s['properties']['notes']={'type':'string'}
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    item['notes']='optional'
    p['field_policy']['exclusions']=[{'path':'notes','reason':'Target has no note equivalent','approved_by':'inventory-domain-owner'}]
    assert apply(p,s,t,item)['unit']=='centimeter'

def test_hidden_renaming_not_identity(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    p['rules'][0]['op']='copy';p['rules'][0]['class']='identity'
    with pytest.raises(MappingError) as e:check_profile(p)
    assert e.value.code=='BURDEN_MISDECLARED'

def test_cannot_relabel_owner(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    p['rules'][-1]['op']='rename';p['rules'][-1]['to']='external_id'
    with pytest.raises(MappingError):check_profile(p)

def test_script_injection_invalid(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    p['rules'][0]['op']='eval'
    with pytest.raises(MappingError):check_profile(p)

def test_pin_change_blocks(tmp_path,foreign_profile):
    import shutil
    dst=tmp_path/'foreign';shutil.copytree(foreign_profile.parent,dst)
    (dst/'target.schema.json').write_text('{}')
    with pytest.raises(MappingError) as e:load_profile(dst/'profile.json')
    assert e.value.code=='CONTRACT_PIN_MISMATCH'

def test_duplicate_destination(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    p['rules'][1]['to']='external_id'
    with pytest.raises(MappingError) as e:check_profile(p)
    assert e.value.code=='MAPPING_COLLISION'

def test_malicious_path(tmp_path,foreign_profile):
    import shutil
    dst=tmp_path/'foreign';shutil.copytree(foreign_profile.parent,dst)
    p=json.loads((dst/'profile.json').read_text())
    p['source_contract']['path']='../../etc/passwd'
    (dst/'profile.json').write_text(json.dumps(p))
    with pytest.raises(MappingError) as e:load_profile(dst/'profile.json')
    assert e.value.code=='MAPPING_PATH_INVALID'

def test_mapping_determinism(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    assert apply(p,s,t,item)==apply(p,s,t,item)

def test_missing_golden_never_marked_verified(foreign_profile):
    report=evaluate(foreign_profile,golden=False)
    assert not report['golden_verified'] and report['coverage']==0

def test_numeric_conversion_with_explicit_factor(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    p['rules'][1]['op']='convert_unit'
    p['rules'][1]['class']='value'
    p['rules'][1]['factor']='100'
    p['rules'][1]['to']='quantity'
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    assert apply(p,s,t,item)['quantity']==1500

def test_offline_schema_never_resolves_http_ref(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    s['$ref']='https://attacker.invalid/do-not-fetch'
    item=load_json(foreign_profile.parent/'examples/golden.input.json')
    with pytest.raises(MappingError) as e:apply(p,s,t,item)
    assert e.value.code=='UNSAFE_SCHEMA_REF'

def test_no_dynamic_schema_ref(foreign_profile):
    p,s,t=load_profile(foreign_profile)
    t['$dynamicRef']='https://attacker.invalid/schema'
    with pytest.raises(MappingError):apply(p,s,t,load_json(foreign_profile.parent/'examples/golden.input.json'))
