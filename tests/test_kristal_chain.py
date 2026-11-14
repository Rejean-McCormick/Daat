"""Security/contract tests for offline DaaT-to-Kristal review handoff.

All tests are synthetic. No real owner checkout or workspace is written.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from daat.candidates import deterministic_candidates
from daat.errors import AdmissionError
from daat.kristal_chain import (discover_roots, owner_preflight,
                                prepare_handoff, verify_handoff)
from daat.review import prepare_review_packet
from daat.source import Evidence, RightsDeclaration, SourceSelection, make_preparation
from daat.util import json_digest


def _preview():
    selection = SourceSelection(
        Path('.'), 'data.json', 'dataset', '01',
        RightsDeclaration('tenant-a', 'local research', 'private licensed', 'reviewer-1', True),
    )
    ev = Evidence(anchor_kind='json_pointer', location='/records/0', source_sha256='a' * 64,
                  record_type='record', data={'id': 'external:12', 'value': 3})
    preview = make_preparation(selection, adapter_id='synthetic', adapter_version='0',
                               records=[ev], source_digest='a' * 64)
    preview['candidates'] = deterministic_candidates(preview)
    preview['preview_sha256'] = json_digest({k:v for k,v in preview.items() if k != 'preview_sha256'})
    return preview


def _review(preview, choice='submit_to_owner'):
    return prepare_review_packet(preview, [dict(candidate_id=preview['candidates'][0]['candidate_id'],
                                                 decision=choice, reason='Reviewed source evidence')],
                                 reviewer='reviewer-1', purpose='private staging')


def test_roundtrip_metadata_only_and_source_data_opt_in():
    preview = _preview(); review = _review(preview)
    packet = prepare_handoff(preview, review)
    assert packet['submitted_count'] == 1
    assert 'source_record_data_unverified' not in packet['submitted_candidates'][0]
    assert packet['owner_contract'] is None
    assert packet['publication_authorized'] is False
    assert verify_handoff(packet, preview=preview, review=review)['valid']
    full = prepare_handoff(preview, review, include_evidence=True)
    assert full['submitted_candidates'][0]['source_record_data_unverified'] == preview['records'][0]['data']
    assert verify_handoff(full, preview=preview, review=review)['source_data_copied']


def test_review_reject_does_not_offer_candidate():
    preview = _preview(); review = _review(preview, choice='reject')
    packet = prepare_handoff(preview, review)
    assert packet['submitted_count'] == 0
    assert packet['rejected_or_deferred_count'] == 1
    assert verify_handoff(packet)['valid']


def test_tampering_and_recomputed_authority_are_denied():
    preview = _preview(); packet = prepare_handoff(preview, _review(preview))
    packet['submitted_count'] = 999
    with pytest.raises(AdmissionError): verify_handoff(packet)
    packet['submitted_count'] = 1
    packet['owner_approval'] = {'granted': True}
    packet['handoff_sha256'] = json_digest({k: v for k, v in packet.items() if k != 'handoff_sha256'})
    with pytest.raises(AdmissionError): verify_handoff(packet)
    packet['owner_approval'] = None
    packet['canonical_graph'] = {'KQ1': 'fake'}
    packet['handoff_sha256'] = json_digest({k:v for k,v in packet.items() if k != 'handoff_sha256'})
    with pytest.raises(AdmissionError): verify_handoff(packet)


def test_recomputed_evidence_or_review_drift_denied():
    preview = _preview(); review = _review(preview)
    preview_other = _preview()
    preview_other['records'][0]['data']['value'] = 7
    preview_other['preview_sha256'] = json_digest({k:v for k,v in preview_other.items() if k != 'preview_sha256'})
    with pytest.raises(AdmissionError):prepare_handoff(preview_other, review)
    packet = prepare_handoff(preview, review)
    review2 = _review(preview, choice='defer')
    with pytest.raises(AdmissionError):verify_handoff(packet, preview=preview, review=review2)


def test_forged_review_candidate_link_denied():
    preview = _preview(); review = _review(preview)
    review['decisions'][0]['evidence_id'] = 'ev-' + 'b' * 64
    review['packet_sha256'] = json_digest({k:v for k,v in review.items() if k != 'packet_sha256'})
    with pytest.raises(AdmissionError):prepare_handoff(preview, review)


def _write(path: Path, data: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding='utf-8')


def _owners(top: Path):
    fw = top / 'Kristal-Framework'; kit = top / 'Kristal-Authoring-Kit'
    _write(fw/'VERSION', '11.0.0-draft.4\n')
    _write(kit/'VERSION', '4.0.0-draft.4\n')
    _write(kit/'tools/kristal.py', '# placeholder owner CLI; never invoked\n')
    files = {}
    paths = ['VERSION', 'schemas/v11/kristal-semantic-graph.schema.json',
             'schemas/v11/kristal-identity-registry.schema.json',
             'schemas/v11/kristal-external-crosswalk.schema.json',
             'schemas/v11/kristal-dictionary-catalog.schema.json'] + [f'tools/v11/synthetic_{i}.py' for i in range(8)]
    for rel in paths:
        if rel != 'VERSION':_write(fw/rel, rel+'\n')
        files[rel] = hashlib.sha256((fw/rel).read_bytes()).hexdigest()
    _write(kit/'contracts/v11-framework-pin.json', json.dumps({
        'profile': 'kristal-integration-framework-pin/v11.0-draft.4',
        'version':'11.0.0-draft.4', 'files':files,
    }))
    _write(top/'Kristalizer/VERSION', '1.2.2\n')
    _write(top/'Kristalizer/kristalizer.py', '# placeholder\n')
    _write(top/'Arketype/AGENTS.md', 'non-normative\n')
    _write(top/'diK/spec/diK-1.0/AGENTS.md', 'diK review only\n')
    return fw,kit


def test_owner_preflight_local_pin_and_dik_blocker():
    with TemporaryDirectory() as d:
        top=Path(d); fw,kit=_owners(top)
        out=owner_preflight(top)
        assert out['checks']['framework']['pinned_files_checked'] == 13
        assert out['checks']['framework']['pin_drift'] == []
        assert out['status'] == 'blocked'  # Semantic/diK compatibility is not owner-qualified
        assert 'dik_draft_compatibility_not_qualified' in out['blockers']
        assert not out['owner_effects_authorized']
        _write(fw/'tools/v11/synthetic_2.py','tampered\n')
        broken=owner_preflight(top)
        assert 'framework_pin_mismatch' in broken['blockers']
        assert 'tools/v11/synthetic_2.py' in broken['checks']['framework']['pin_drift']


def test_owner_preflight_fails_closed_missing_or_unapproved_version():
    with TemporaryDirectory() as d:
        top=Path(d);fw,kit=_owners(top)
        _write(kit/'VERSION','4.0.0-draft.5\n')
        out=owner_preflight(top)
        assert 'unapproved_kit_version' in out['blockers']
        (kit/'contracts/v11-framework-pin.json').unlink()
        out=owner_preflight(top)
        assert 'framework_pin_verification_failed' in out['blockers']


def test_owner_discovery_rejects_duplicate_root_and_symlink():
    with TemporaryDirectory() as d:
        top=Path(d);_owners(top)
        with pytest.raises(AdmissionError): discover_roots(top, overrides={'framework':top/'Kristal-Framework','kit':top/'Kristal-Framework'})
        link=top/'linked-kit'
        try:link.symlink_to(top/'Kristal-Authoring-Kit', target_is_directory=True)
        except (OSError,NotImplementedError):return
        with pytest.raises(AdmissionError): discover_roots(top, overrides={'kit':link})


def test_cli_prepare_handoff_and_verify_with_paths(tmp_path, capsys):
    from daat.cli import main
    preview=_preview();review=_review(preview)
    p=tmp_path/'preview.json';r=tmp_path/'review.json';o=tmp_path/'proposal.json'
    p.write_text(json.dumps(preview),encoding='utf-8');r.write_text(json.dumps(review),encoding='utf-8')
    assert main(['kristal-prepare-handoff','--preview',str(p),'--review',str(r),'--out',str(o)]) == 0
    assert o.exists()
    assert main(['kristal-verify-handoff','--handoff',str(o),'--preview',str(p),'--review',str(r)]) == 0
    assert main(['kristal-verify-handoff','--handoff',str(o),'--preview',str(p)]) == 2


def test_local_handoff_prototype_schema(tmp_path):
    import jsonschema
    schema_path = Path(__file__).resolve().parents[1] / 'contracts/daat/kristal-review-handoff.prototype.schema.json'
    schema=json.loads(schema_path.read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator.check_schema(schema)
    preview=_preview();packet=prepare_handoff(preview,_review(preview))
    jsonschema.validate(packet, schema)
    packet2=prepare_handoff(preview,_review(preview),include_evidence=True)
    jsonschema.validate(packet2, schema)
    packet2['owner_approval']={'granted':True}
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(packet2,schema)
