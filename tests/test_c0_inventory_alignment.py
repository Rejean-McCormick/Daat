"""Contract-oriented negative fixtures for kOA C0 checkout location hints.

No network, Kit subprocess, owner workspace writes or publication are used.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from daat.errors import AdmissionError
from daat.owner_inventory import read_c0_owner_hints
from daat.kristal_chain import discover_roots, dik_v11_schema_parity

INVENTORY = 'kOA_Digital_Ecosystem/kOA_Digital_Ecosystem/docs/inventory/repositories.json'


def _save_inventory(root: Path, rows):
    p = root / INVENTORY
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rows), encoding='utf-8')
    return p


def _row(repo, loc):
    return {'github_repo': f'Rejean-McCormick/{repo}', 'local_root': loc,
            'scope': 'PUBLIC', 'status': 'github_and_local_remote_verified'}


def test_c0_nested_owner_paths_resolve_from_documented_inventory(tmp_path):
    rows = [
        _row('Daat', r'C:\mycode\Interaction-Kernel\Daat'),
        _row('Kristal-Framework', r'C:\mycode\Kristal\Kristal-Framework'),
        _row('Kristal-Authoring-Kit', r'C:\mycode\Kristal\Kristal-Authoring-Kit'),
        _row('Arketype', r'C:\mycode\Kristal\Arketype\arketype'),
        _row('diK', r'C:\mycode\diK\diK'),
    ]
    p = _save_inventory(tmp_path, rows)
    hint = read_c0_owner_hints(tmp_path)
    assert hint['inventory_sha256'] == hashlib.sha256(p.read_bytes()).hexdigest()
    assert hint['paths_by_role']['daat'] == tmp_path/'Interaction-Kernel/Daat'
    assert hint['paths_by_role']['arketype'] == tmp_path/'Kristal/Arketype/arketype'
    assert hint['owner_authority_granted'] is False
    # Read-only resolution never asserts semantic authority.
    fw = tmp_path/'Kristal/Kristal-Framework'
    fw.mkdir(parents=True)
    (fw/'VERSION').write_text('11.0.0-draft.4', encoding='utf-8')
    (fw/'schemas/v11').mkdir(parents=True)
    (fw/'schemas/v11/kristal-semantic-graph.schema.json').write_text('{}', encoding='utf-8')
    root = discover_roots(tmp_path)
    assert root['framework'] == fw
    assert root['kit'] is None


@pytest.mark.parametrize('injected', [
    r'D:\somewhere\Daat',
    r'\\server\share\Daat',
    r'C:\other\Daat',
    r'C:\mycode\..\secrets\Daat',
    r'..\Daat',
])
def test_c0_inventory_denies_untrusted_path(injected, tmp_path):
    _save_inventory(tmp_path, [_row('Daat', injected)])
    with pytest.raises(AdmissionError): read_c0_owner_hints(tmp_path)


def test_c0_duplicate_identity_refused(tmp_path):
    _save_inventory(tmp_path, [_row('Daat',r'C:\mycode\Interaction-Kernel\Daat')]*2)
    with pytest.raises(AdmissionError): read_c0_owner_hints(tmp_path)


def test_c0_inventory_explicit_missing_does_not_silently_fallback(tmp_path):
    with pytest.raises(AdmissionError): read_c0_owner_hints(tmp_path, 'no-such.json')
    assert read_c0_owner_hints(tmp_path) is None


def test_c0_inventory_cannot_use_symlink_to_escape(tmp_path):
    outside = tmp_path.parent/'outside-inventory'
    outside.mkdir(exist_ok=True)
    target = outside/'repositories.json'
    target.write_text('[]', encoding='utf-8')
    dest = tmp_path/INVENTORY
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        dest.symlink_to(target)
    except (OSError, NotImplementedError):
        return
    with pytest.raises(AdmissionError): read_c0_owner_hints(tmp_path)


def test_dik_schema_parity_is_byte_only_and_fails_on_tamper(tmp_path):
    fw = tmp_path/'framework'; dik = tmp_path/'dik'
    (fw/'schemas/v11').mkdir(parents=True)
    (dik/'src/dik/_framework/schemas/v11').mkdir(parents=True)
    (dik/'pyproject.toml').write_text('[project]\nversion = "1.0.0a7"\n', encoding='utf-8')
    for i in range(11):
        name = f'schema-{i}.schema.json'
        (fw/'schemas/v11'/name).write_text('{"type":"object"}', encoding='utf-8')
        (dik/'src/dik/_framework/schemas/v11'/name).write_text('{"type":"object"}', encoding='utf-8')
    found = dik_v11_schema_parity(fw, dik)
    assert found['schema_byte_parity'] is True
    assert found['compared_schema_count'] == 11
    assert 'not_functional' in found['parity_scope']
    (dik/'src/dik/_framework/schemas/v11/schema-4.schema.json').write_text('replaced', encoding='utf-8')
    found = dik_v11_schema_parity(fw, dik)
    assert found['schema_byte_parity'] is False
    assert found['schema_drift'] == ['schema-4.schema.json']


def test_dik_wrong_version_does_not_claim_parity(tmp_path):
    fw = tmp_path/'framework'; dik = tmp_path/'dik'
    fw.mkdir();dik.mkdir()
    (dik/'pyproject.toml').write_text('[project]\nversion = "2.0.0"\n', encoding='utf-8')
    found = dik_v11_schema_parity(fw, dik)
    assert found['schema_byte_parity'] is False
    assert found['reason'] == 'unexpected_dik_version'


def test_cli_owner_locations_readonly(tmp_path, capsys):
    from daat.cli import main
    _save_inventory(tmp_path, [_row('Daat', r'C:\mycode\Interaction-Kernel\Daat')])
    assert main(['kristal-owner-locations','--root',str(tmp_path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output['paths_by_role']['daat'] == str(tmp_path/'Interaction-Kernel/Daat')
    assert output['owner_authority_granted'] is False
