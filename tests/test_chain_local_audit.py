"""DaAT 0.4.3 local chain audit and fail-closed review regression tests."""
from __future__ import annotations
import json
from pathlib import Path
import pytest
from daat.errors import AdmissionError
from daat.util import json_digest
from daat.chain_audit import audit_local_chain
from daat.review import verify_review_packet, prepare_review_packet
from daat.kristal_chain import prepare_handoff, verify_handoff
from daat.source import RightsDeclaration, SourceSelection, Evidence, make_preparation
from daat.candidates import deterministic_candidates


def fixture():
    sel=SourceSelection(Path('.'), 'data.json','dataset','01',
        RightsDeclaration('tenant-s','synthetic','self-created','reviewer-1',True))
    ev=Evidence(anchor_kind='json_pointer', location='/row/0',source_sha256='a'*64,
                record_type='record',data={'id':'reference-1','value':42})
    preview=make_preparation(sel,adapter_id='synthetic',adapter_version='1',records=[ev],source_digest='a'*64)
    preview['candidates']=deterministic_candidates(preview)
    preview['preview_sha256']=json_digest({k:v for k,v in preview.items() if k!='preview_sha256'})
    decisions=[{'candidate_id':preview['candidates'][0]['candidate_id'],
                'decision':'submit_to_owner','reason':'Synthetic source checked'}]
    review=prepare_review_packet(preview,decisions,reviewer='reviewer-1',purpose='synthetic-only')
    handoff=prepare_handoff(preview,review)
    return preview,review,handoff


def reseal(packet, field):
    packet[field]=json_digest({k:v for k,v in packet.items() if k!=field})


def test_audit_reports_only_local_verified_and_no_source_bytes():
    p,r,h=fixture()
    a=audit_local_chain(p,r,h)
    assert a['status']=='local_chain_verified_not_owner_approved'
    assert a['local_integrity']=={'preview':True,'review':True,'handoff':True}
    assert a['owner_admission']=='not_qualified'
    assert a['owner_pin_preflight']['status']=='not_requested'
    assert a['canonical_kristal_created'] is False
    assert 'reference-1' not in json.dumps(a)
    assert a['audit_sha256']==json_digest({k:v for k,v in a.items() if k!='audit_sha256'})


@pytest.mark.parametrize('change', ['unexpected_field','duplicate','bad_evidence','bad_reason','bad_reviewer','bad_count'])
def test_recomputed_review_hash_cannot_sneak_illegal_structure(change):
    p,r,h=fixture()
    if change=='unexpected_field':r['owner_receipt']={'trusted':True}
    if change=='duplicate':r['decisions'].append(dict(r['decisions'][0]))
    if change=='bad_evidence':r['decisions'][0]['evidence_id']='ev-not-a-valid-digest'
    if change=='bad_reason':r['decisions'][0]['reason']='x'
    if change=='bad_reviewer':r['reviewer_assertion']='fake actor'
    if change=='bad_count':r['unreviewed_candidate_ids']=[r['decisions'][0]['candidate_id']]
    reseal(r,'packet_sha256')
    with pytest.raises(AdmissionError):verify_review_packet(r)
    with pytest.raises(AdmissionError):audit_local_chain(p,r,h)


def test_exact_source_binding_fails_when_review_edited_even_resealed():
    p,r,h=fixture()
    r['decisions'][0]['reason']='Different reason, after initial handoff'
    reseal(r,'packet_sha256')
    assert verify_review_packet(r)['valid']
    with pytest.raises(AdmissionError):audit_local_chain(p,r,h)


def test_handoff_recomputed_hash_rejects_semantic_authority_and_bad_hints():
    p,r,h=fixture()
    h['submitted_candidates'][0]['proposed_arketypes']=['KQ-fake']
    reseal(h,'handoff_sha256')
    with pytest.raises(AdmissionError):verify_handoff(h)


def test_cli_local_chain_audit(tmp_path,capsys):
    from daat.cli import main
    p,r,h=fixture()
    for name,data in [('preview.json',p),('review.json',r),('handoff.json',h)]:
        (tmp_path/name).write_text(json.dumps(data),encoding='utf-8')
    out=tmp_path/'audit.json'
    assert main(['kristal-local-chain-audit','--preview',str(tmp_path/'preview.json'),
                 '--review',str(tmp_path/'review.json'),'--handoff',str(tmp_path/'handoff.json'),
                 '--out',str(out)])==0
    assert json.loads(out.read_text())['owner_admission']=='not_qualified'
