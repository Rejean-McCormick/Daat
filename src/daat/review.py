"""Local reviewer queue/packet; not a Kristalizer or Kit contract.

Human acceptance here means only "ready to offer to a governed owner". It is
never sufficient for canonical semantic identities, builds or publication.
"""
from __future__ import annotations
import re
from typing import Any, Iterable

from .errors import AdmissionError
from .util import json_digest
from .verification import verify_preparation

_REVIEWER = re.compile("^[a-zA-Z0-9_.:/-]{2,128}$")
_CHOICES = {"submit_to_owner", "reject", "defer"}
_CANDIDATE = re.compile(r"^cand-[a-f0-9]{64}$")
_EVIDENCE = re.compile(r"^ev-[a-f0-9]{64}$")
_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_REVIEW_FIELDS = {"format", "state", "preview_sha256", "source_manifest_sha256",
                  "reviewer_assertion", "purpose", "decisions", "unreviewed_candidate_ids",
                  "owner_approval", "owner_contract", "publication_authorized", "packet_sha256"}


def prepare_review_packet(preview: dict[str, Any], decisions: Iterable[dict[str, Any]],
                          *, reviewer: str, purpose: str) -> dict[str, Any]:
    verify_preparation(preview)
    if not _REVIEWER.fullmatch(reviewer) or not purpose.strip() or len(purpose) > 250:
        raise AdmissionError("REVIEW_INVALID", "Explicit reviewer and bounded purpose required")
    candidates = {c["candidate_id"]: c for c in preview.get("candidates", [])}
    reviewed: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in decisions:
        if not isinstance(item, dict) or set(item) != {"candidate_id", "decision", "reason"}:
            raise AdmissionError("REVIEW_INVALID", "Review must use candidate_id, decision and reason")
        ident = item["candidate_id"]
        if ident not in candidates or ident in seen or item["decision"] not in _CHOICES:
            raise AdmissionError("REVIEW_INVALID", "Unknown/repeated candidate or invalid decision")
        if not isinstance(item["reason"], str) or len(item["reason"].strip()) < 5 or len(item["reason"]) > 1000:
            raise AdmissionError("REVIEW_INVALID", "Specific bounded review reason required")
        seen.add(ident)
        reviewed.append({"candidate_id": ident, "evidence_id": candidates[ident]["evidence_id"],
                         "decision": item["decision"], "reason": item["reason"]})
    missing = sorted(set(candidates) - seen)
    packet = {
        "format": "daat.local-review-packet/0.1.0-prototype",
        "state": "local_unverified_review_not_kit_admission",
        "preview_sha256": preview["preview_sha256"],
        "source_manifest_sha256": preview["source"]["manifest_sha256"],
        "reviewer_assertion": reviewer, "purpose": purpose,
        "decisions": reviewed,
        "unreviewed_candidate_ids": missing,
        "owner_approval": None, "owner_contract": None,
        "publication_authorized": False,
    }
    packet["packet_sha256"] = json_digest(packet)
    return packet


def verify_review_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Reject forged review structure even when an attacker recomputes the local hash.

    Without the original preview, candidate/evidence equivalence is *not* proved.
    Consumers must pass both preview and review to prepare_handoff.
    """
    if not isinstance(packet, dict) or set(packet) != _REVIEW_FIELDS:
        raise AdmissionError("REVIEW_INVALID", "Missing or undeclared review packet fields")
    if packet["format"] != "daat.local-review-packet/0.1.0-prototype":
        raise AdmissionError("REVIEW_INVALID", "Not a supported review packet")
    if (packet["owner_approval"] is not None or packet["owner_contract"] is not None or
            packet["publication_authorized"] is not False or
            packet["state"] != "local_unverified_review_not_kit_admission"):
        raise AdmissionError("REVIEW_AUTHORITY_INVALID", "Local review cannot confer owner authority")
    for key in ("preview_sha256", "source_manifest_sha256", "packet_sha256"):
        if not isinstance(packet[key], str) or not _SHA256.fullmatch(packet[key]):
            raise AdmissionError("REVIEW_INVALID", "Invalid local digest field")
    reviewer, purpose = packet["reviewer_assertion"], packet["purpose"]
    if (not isinstance(reviewer, str) or not _REVIEWER.fullmatch(reviewer)
            or not isinstance(purpose, str) or not purpose.strip() or len(purpose) > 250):
        raise AdmissionError("REVIEW_INVALID", "Reviewer assertion or purpose is invalid")
    decisions, unreviewed = packet["decisions"], packet["unreviewed_candidate_ids"]
    if (not isinstance(decisions, list) or not isinstance(unreviewed, list)
            or len(decisions) > 10_000 or len(unreviewed) > 10_000):
        raise AdmissionError("REVIEW_INVALID", "Review candidate lists are invalid or unbounded")
    seen: set[str] = set()
    for row in decisions:
        if not isinstance(row, dict) or set(row) != {"candidate_id", "evidence_id", "decision", "reason"}:
            raise AdmissionError("REVIEW_INVALID", "Invalid decision fields")
        ident, ev = row["candidate_id"], row["evidence_id"]
        if (not isinstance(ident, str) or not _CANDIDATE.fullmatch(ident)
                or not isinstance(ev, str) or not _EVIDENCE.fullmatch(ev)
                or ident in seen or row["decision"] not in _CHOICES
                or not isinstance(row["reason"], str)
                or not 5 <= len(row["reason"].strip()) <= 1000):
            raise AdmissionError("REVIEW_INVALID", "Invalid/duplicate decision or evidence reference")
        seen.add(ident)
    for ident in unreviewed:
        if not isinstance(ident, str) or not _CANDIDATE.fullmatch(ident) or ident in seen:
            raise AdmissionError("REVIEW_INVALID", "Invalid or duplicate unreviewed candidate")
        seen.add(ident)
    data = dict(packet)
    digest = data.pop("packet_sha256")
    if digest != json_digest(data):
        raise AdmissionError("REVIEW_INTEGRITY", "Review packet digest mismatch")
    return {"valid": True, "packet_sha256": digest, "decisions": len(decisions),
            "authority": "unverified_local_review"}
