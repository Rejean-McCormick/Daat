"""Noncanonical candidate classification and explicitly untrusted AI suggestions.

Arketype IDs are merely design hints. DaaT never mints or recognizes KQ/KP/KA/KS.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import re
from typing import Any, Iterable, Mapping

from .catalog import source_family
from .errors import AdmissionError
from .util import json_digest

_SEMANTIC_ID = re.compile(r"\b(?:KQ|KP|KA|KS)[-:]?[0-9a-z]+\b", flags=re.I)


def deterministic_candidates(preview: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Create a review queue, never inferred factual claims or canonical identities."""
    src = preview["source"]
    family = source_family(src["family_id"])
    proposals: list[dict[str, Any]] = []
    for record in preview["records"]:
        entry: dict[str, Any] = {
            "evidence_id": record["local_evidence_id"],
            "candidate_type": record["record_type"],
            "source_location": record["anchor"],
            "source_sha256": record["source_sha256"],
            "proposed_arketypes": list(family.candidate_arketypes),
            "review_state": "pending_owner_review_noncanonical",
            "semantic_identity": None,
            "origin": "deterministic_source_shape_only",
        }
        data = record["data"]
        # External identifiers retained without treating same labels or DOI as equivalence.
        external: dict[str, Any] = {}
        for key in ("doi", "DOI", "orcid", "isbn", "id", "invoice_id", "commit", "blob_id"):
            if key in data and isinstance(data[key], (str, int)):
                external[key] = str(data[key])
        if external:
            entry["external_identifiers_unreviewed"] = external
        entry["candidate_id"] = "cand-" + json_digest(entry)
        proposals.append(entry)
    return proposals


def _reject_canonical_keys(data: Any) -> None:
    forbidden = {"kq", "kp", "ka", "ks", "kristal_state", "canonical", "published",
                 "recognized", "validated", "actionability", "release_authorization"}
    if isinstance(data, dict):
        if any(str(k).lower() in forbidden for k in data):
            raise AdmissionError("AI_CANDIDATE_UNSAFE", "AI attempted to set owned semantic/authority fields")
        for v in data.values():
            _reject_canonical_keys(v)
    elif isinstance(data, list):
        for v in data:
            _reject_canonical_keys(v)


def attach_ai_suggestions(preview: dict[str, Any], suggestions: Iterable[dict[str, Any]],
                          *, model_id: str, model_version: str,
                          authorized_review: bool = False) -> dict[str, Any]:
    """Attach host-reviewed model output as untrusted candidates (never owner effect).

    AI/network clients are not inside DaaT. The caller must separately enforce
    grants, tenant boundaries, model privacy, prompt safety and audit.
    """
    if not authorized_review:
        raise AdmissionError("AI_CANDIDATE_UNTRUSTED", "A trusted review host must opt in to AI candidate attachment")
    if not model_id or not model_version or len(model_id) > 128 or len(model_version) > 128:
        raise AdmissionError("AI_CANDIDATE_INVALID", "Model identity and version required")
    existing = {rec["local_evidence_id"] for rec in preview.get("records", ())}
    prepared: list[dict[str, Any]] = []
    for raw in suggestions:
        if not isinstance(raw, dict) or set(raw) != {"evidence_id", "suggestion", "confidence"}:
            raise AdmissionError("AI_CANDIDATE_INVALID", "AI suggestion must have exact bounded fields")
        if raw["evidence_id"] not in existing:
            raise AdmissionError("AI_CITATION_INVALID", "AI evidence reference not present in preview")
        content = raw["suggestion"]
        if not isinstance(content, str) or not content.strip() or len(content) > 4000:
            raise AdmissionError("AI_CANDIDATE_INVALID", "Invalid AI candidate text length")
        if _SEMANTIC_ID.search(content):
            raise AdmissionError("AI_CANDIDATE_UNSAFE", "AI cannot assert Kristal identities")
        confidence = raw["confidence"]
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            raise AdmissionError("AI_CANDIDATE_INVALID", "Confidence must be in [0,1]")
        candidate = {
            "evidence_id": raw["evidence_id"], "suggestion": content,
            "model_confidence_unverified": confidence,
            "model_id": model_id, "model_version": model_version,
            "review_state": "unreviewed_ai_suggestion",
            "semantic_identity": None,
        }
        candidate["candidate_id"] = "ai-" + json_digest(candidate)
        prepared.append(candidate)
    result = dict(preview)
    result["ai_suggestions"] = prepared
    result.pop("preview_sha256", None)
    result["preview_sha256"] = json_digest(result)
    return result
