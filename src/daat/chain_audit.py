"""Offline, reproducible local DaAT package audit (never an owner acceptance).

This checks exact preview/review/handoff binding and optionally reads owner
version pins. It does not execute any owner CLI or produce a Kristal state.
"""
from __future__ import annotations

from typing import Any
from pathlib import Path

from .kristal_chain import owner_preflight, verify_handoff
from .review import verify_review_packet
from .verification import verify_preparation
from .util import json_digest


def audit_local_chain(preview: dict[str, Any], review: dict[str, Any],
                      handoff: dict[str, Any], *, owner_root: Path | str | None = None,
                      inventory: Path | str | None = None) -> dict[str, Any]:
    """Fail closed on local input changes; report *no* source-record payload."""
    source = verify_preparation(preview)
    reviewer = verify_review_packet(review)
    proposal = verify_handoff(handoff, preview=preview, review=review)
    owner = owner_preflight(owner_root, inventory=inventory) if owner_root is not None else None
    result: dict[str, Any] = {
        "format": "daat.local-chain-audit/0.1.0-prototype",
        "status": "local_chain_verified_not_owner_approved",
        "local_integrity": {"preview": source["valid"], "review": reviewer["valid"],
                            "handoff": proposal["valid"]},
        "references": {"preview_sha256": preview["preview_sha256"],
                       "review_sha256": review["packet_sha256"],
                       "handoff_sha256": handoff["handoff_sha256"]},
        "counts": {"records": source["records"], "candidates": source["candidates"],
                   "decisions": reviewer["decisions"], "submitted": proposal["submitted_count"]},
        "owner_pin_preflight": ({"status": owner["status"],
                                 "blockers": owner["blockers"],
                                 "verification_level": owner["verification_level"]}
                                if owner else {"status": "not_requested"}),
        "external_owner_effects": "not_executed",
        "owner_admission": "not_qualified",
        "canonical_kristal_created": False,
        "published": False,
        "activated": False,
    }
    result["audit_sha256"] = json_digest(result)
    return result
