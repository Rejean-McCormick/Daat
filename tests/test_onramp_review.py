from __future__ import annotations
import json
import pytest
from daat.source import SourceSelection, RightsDeclaration
from daat.pipeline import prepare_local
from daat.candidates import attach_ai_suggestions
from daat.review import prepare_review_packet, verify_review_packet
from daat.verification import verify_preparation
from daat.errors import AdmissionError


@pytest.fixture
def sample_preview(tmp_path):
    (tmp_path / "file.jsonl").write_text('{"title":"An external title","doi":"10.1234/abc"}\n', encoding="utf-8")
    source = SourceSelection(tmp_path, "file.jsonl", "dataset", "07",
                             RightsDeclaration("tenant-1", "sample", "owned", "actor-1", True))
    return prepare_local(source)


def test_ai_suggestions_require_host_review_and_valid_evidence(sample_preview):
    eid = sample_preview["records"][0]["local_evidence_id"]
    item = {"evidence_id": eid, "suggestion": "Investigate two possible authors", "confidence": 0.5}
    with pytest.raises(AdmissionError):
        attach_ai_suggestions(sample_preview, [item], model_id="review-model", model_version="1")
    enhanced = attach_ai_suggestions(sample_preview, [item], model_id="review-model",
                                      model_version="1", authorized_review=True)
    assert enhanced["ai_suggestions"][0]["review_state"] == "unreviewed_ai_suggestion"
    assert verify_preparation(enhanced)["valid"]


def test_ai_rejects_canonical_identity_and_fabricated_citations(sample_preview):
    eid = sample_preview["records"][0]["local_evidence_id"]
    kwargs = dict(model_id="model", model_version="1", authorized_review=True)
    with pytest.raises(AdmissionError):
        attach_ai_suggestions(sample_preview, [{"evidence_id": eid, "suggestion": "Mint KQ-123", "confidence": .8}], **kwargs)
    with pytest.raises(AdmissionError):
        attach_ai_suggestions(sample_preview, [{"evidence_id": "fake", "suggestion": "Unknown", "confidence": .4}], **kwargs)


def test_review_never_grants_kit_approval(sample_preview):
    candidate = sample_preview["candidates"][0]["candidate_id"]
    decisions = [{"candidate_id": candidate, "decision": "submit_to_owner", "reason": "Review with Kit owner"}]
    packet = prepare_review_packet(sample_preview, decisions, reviewer="local-reviewer", purpose="source-review")
    assert packet["owner_approval"] is None
    assert packet["publication_authorized"] is False
    assert verify_review_packet(packet)["valid"]
    packet["owner_approval"] = "granted"
    with pytest.raises(AdmissionError):
        verify_review_packet(packet)


def test_review_invalid_candidates_rejected(sample_preview):
    with pytest.raises(AdmissionError):
        prepare_review_packet(sample_preview, [{"candidate_id": "not-real", "decision": "submit_to_owner",
                                                "reason": "Unverified candidate"}], reviewer="person-a", purpose="test")
