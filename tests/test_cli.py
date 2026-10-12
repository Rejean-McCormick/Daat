import subprocess
import sys
import json

def run(*args):
    return subprocess.run([sys.executable,'-m','daat',*map(str,args)],capture_output=True,text=True)

def test_verify_contracts():
    r=run('verify-contracts')
    assert r.returncode==0 and json.loads(r.stdout)['baseline']=='verified'

def test_map(foreign_profile):
    r=run('map',foreign_profile,foreign_profile.parent/'examples/golden.input.json')
    assert r.returncode==0
    assert json.loads(r.stdout)['unit']=='centimeter'

def test_invalid_build(root):
    r=run('validate-build',root/'mappings/native/examples/golden.input.json')
    assert r.returncode==2

def test_validate_mapping(foreign_profile):
    r=run('validate-mapping',foreign_profile)
    assert r.returncode==0

def test_alignment_report(foreign_profile,tmp_path):
    path=tmp_path/'alignment.json'
    r=run('alignment-report',foreign_profile,'--out',path)
    assert r.returncode==0 and json.loads(path.read_text())['burden_points']==4
