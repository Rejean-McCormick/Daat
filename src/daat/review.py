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
    if packet.get("format") != "daat.local-review-packet/0.1.0-prototype":
        raise AdmissionError("REVIEW_INVALID", "Not a supported review packet")
    if (packet.get("owner_approval") is not None or packet.get("owner_contract") is not None or
            packet.get("publication_authorized") is not False or
            packet.get("state") != "local_unverified_review_not_kit_admission"):
        raise AdmissionError("REVIEW_AUTHORITY_INVALID", "Local review cannot confer owner authority")
    data = dict(packet)
    digest = data.pop("packet_sha256", None)
    if digest != json_digest(data):
        raise AdmissionError("REVIEW_INTEGRITY", "Review packet digest mismatch")
    return {"valid": True, "packet_sha256": digest, "decisions": len(packet.get("decisions", [])),
            "authority": "unverified_local_review"}
