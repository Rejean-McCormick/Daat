"""Validate DaaT local preview and local evidence content digests.

This is an offline integrity check, not a policy grant, claim verification,
cryptographic source signature or owner TCK.
"""
from __future__ import annotations
import re
from typing import Any

from .errors import AdmissionError
from .util import json_digest

_SHA = re.compile("^[0-9a-f]{64}$")


def verify_preparation(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict) or data.get("format") != "daat.local-evidence-preview/0.1.0-prototype":
        raise AdmissionError("PREVIEW_INVALID", "Unsupported local preview format")
    if data.get("authority") != "noncanonical_unreviewed" or data.get("owner_handoff") != "blocked_pending_owner_adopted_contract":
        raise AdmissionError("PREVIEW_INVALID", "Preview tries to assert owner authority")
    marker = data.get("preview_sha256")
    if not isinstance(marker, str) or not _SHA.fullmatch(marker):
        raise AdmissionError("PREVIEW_INVALID", "Preview checksum absent")
    actual = dict(data)
    actual.pop("preview_sha256")
    if json_digest(actual) != marker:
        raise AdmissionError("PREVIEW_INTEGRITY", "Preview content digest mismatch")
    records = data.get("records")
    if not isinstance(records, list):
        raise AdmissionError("PREVIEW_INVALID", "Preview records missing")
    observed_ids = set()
    for record in records:
        if not isinstance(record, dict) or "local_evidence_id" not in record:
            raise AdmissionError("PREVIEW_INVALID", "Malformed evidence record")
        evid = record["local_evidence_id"]
        inner = dict(record)
        inner.pop("local_evidence_id", None)
        if evid != "ev-" + json_digest(inner) or evid in observed_ids:
            raise AdmissionError("PREVIEW_INTEGRITY", "Evidence record invalid or duplicated")
        observed_ids.add(evid)
        if not isinstance(inner.get("source_sha256"), str) or not _SHA.fullmatch(inner["source_sha256"]):
            raise AdmissionError("PREVIEW_INVALID", "Evidence source byte hash missing")
    for candidate in data.get("candidates", []):
        if candidate.get("evidence_id") not in observed_ids or candidate.get("semantic_identity") is not None:
            raise AdmissionError("PREVIEW_INVALID", "Candidate lacks anchor or illegally claims identity")
        claim = dict(candidate)
        digest = claim.pop("candidate_id", None)
        if digest != "cand-" + json_digest(claim):
            raise AdmissionError("PREVIEW_INTEGRITY", "Candidate digest mismatch")
    for candidate in data.get("ai_suggestions", []):
        if candidate.get("evidence_id") not in observed_ids or candidate.get("semantic_identity") is not None:
            raise AdmissionError("PREVIEW_INVALID", "AI candidate lacks evidence or claims identity")
        claim = dict(candidate)
        ident = claim.pop("candidate_id", None)
        if ident != "ai-" + json_digest(claim):
            raise AdmissionError("PREVIEW_INTEGRITY", "AI candidate digest mismatch")
    return {"valid": True, "records": len(records), "candidates": len(data.get("candidates", [])),
            "preview_sha256": marker, "authority": "noncanonical_unreviewed"}
