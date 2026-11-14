"""Offline source-to-candidate engine; *no owner side effects*.

Not an IK transport, source custodian, job scheduler, provenance authority or
Kristal authoring runtime. No caller input can activate a blocked integration.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any

from .candidates import deterministic_candidates
from .errors import AdmissionError
from .mapping import apply, load_profile
from .registry import AdapterRegistry, builtin_registry
from .source import SourceSelection, Evidence, bounded_file_digest, make_preparation
from .util import json_digest


def prepare_local(selection: SourceSelection, *, registry: AdapterRegistry | None = None,
                  mapping_profile: Path | None = None, candidates: bool = True) -> dict[str, Any]:
    """Prepare source evidence for human/owner review, without writing canonical state."""
    selected, reader = (registry or builtin_registry()).resolve(selection)
    if selection.mode == "reference":
        if selection.kind == "git":
            raise AdmissionError("SOURCE_MODE_UNSUPPORTED", "Git reference preview requires pinned snapshot mode")
        digest = bounded_file_digest(selection.path(), max_bytes=selection.limits.max_source_bytes)
        extracted: list[Evidence] = []
        warnings = ["reference_only_no_content_extraction"]
        revision = selection.revision
    else:
        extracted, digest, warnings, revision = reader(selection)
    result = make_preparation(selection, adapter_id=selected["id"], adapter_version=selected["version"],
                              records=extracted, source_digest=digest, warnings=warnings,
                              source_revision=revision)
    result["source"]["mode"] = selection.mode
    result["source"]["record_type"] = selection.record_type
    result["extraction"]["adapter_manifest_sha256"] = json_digest(selected)
    if candidates and selection.mode != "reference":
        result["candidates"] = deterministic_candidates(result)
    if mapping_profile is not None:
        if selection.mode == "reference":
            raise AdmissionError("MAPPING_UNSUPPORTED", "No records can be mapped in reference-only mode")
        profile, source_schema, target_schema = load_profile(mapping_profile)
        transformed = []
        for item in result["records"]:
            mapped = apply(profile, source_schema, target_schema, item["data"])
            transformed.append({"evidence_id": item["local_evidence_id"], "mapped": mapped,
                                "status": "local_candidate_not_an_owner_build"})
        result["mapping_preview"] = {
            "profile": profile["id"] + "/" + profile["version"],
            "source_contract_sha256": profile["source_contract"]["sha256"],
            "target_contract_sha256": profile["target_contract"]["sha256"],
            "records": transformed,
            "target_authority": "none_owner_import_not_approved",
        }
    result.pop("preview_sha256", None)
    result["preview_sha256"] = json_digest(result)
    return result


def concise_report(preview: dict[str, Any]) -> dict[str, Any]:
    """Safe-to-print summary without raw extracted content or personal records."""
    return {
        "format": preview["format"], "status": preview["authority"],
        "source_kind": preview["source"]["kind"],
        "family_id": preview["source"]["family_id"],
        "mode": preview["source"]["mode"],
        "adapter": preview["extraction"]["adapter_id"],
        "record_count": len(preview["records"]),
        "candidate_count": len(preview.get("candidates", [])),
        "warning_count": len(preview.get("warnings", [])),
        "source_manifest_sha256": preview["source"]["manifest_sha256"],
        "preview_sha256": preview["preview_sha256"],
        "owner_handoff": preview["owner_handoff"],
    }
