"""Deterministic local source-shape hints: never semantic identity or access rights."""
from __future__ import annotations
from pathlib import Path
from typing import Any

from .errors import AdmissionError
from .source import RightsDeclaration, confined_path

_EXTENSION_HINTS = {
    ".pdf": ("pdf", ["08", "02", "09", "21", "22", "28"], "L1"),
    ".zip": ("archive", ["09", "08", "28"], "L1"),
    ".json": ("dataset", ["07", "16", "30", "01"], "L1"),
    ".jsonl": ("dataset", ["07", "16", "26", "01"], "L1"),
    ".csv": ("dataset", ["07", "13", "16", "01"], "L1"),
    ".tsv": ("dataset", ["07", "13", "16", "01"], "L1"),
    ".ris": ("bibliography", ["01", "02", "03"], "L1"),
    ".xml": ("bibliography", ["01", "02", "03", "20"], "L1"),
}


def diagnose_local(root: Path, relative_path: str, rights: RightsDeclaration) -> dict[str, Any]:
    # The rights declaration validates independently. This is never an owner grant.
    if not rights.permission_asserted:
        raise AdmissionError("RIGHTS_NOT_ASSERTED", "Local source rights must be asserted")
    path = confined_path(root, relative_path, allow_directory=True)
    if path.is_dir():
        if not (path / ".git").is_dir() or (path / ".git").is_symlink():
            return {"status": "unsupported_directory", "candidates": [],
                    "note": "Use explicitly permitted files or an immutable local Git checkout"}
        hints = ("git", ["11", "12"], "L5")
    else:
        hints = _EXTENSION_HINTS.get(path.suffix.lower())
        if hints is None:
            return {"status": "no_supported_reader_for_extension", "candidates": [],
                    "note": "Reference-only via approved host is still possible"}
        with path.open("rb") as f:
            magic = f.read(8)
        if hints[0] == "pdf" and not magic.startswith(b"%PDF-"):
            raise AdmissionError("SOURCE_PDF_INVALID", "Source extension and PDF magic disagree")
        if hints[0] == "archive" and not magic.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")):
            raise AdmissionError("SOURCE_ARCHIVE_INVALID", "ZIP header and extension disagree")
    kind, families, lane = hints
    return {
        "status": "source_shape_candidates_only",
        "source_kind_hint": kind,
        "access_lane_hint": lane,
        "candidates": [{"family_id": fid, "verification": "heuristic_unreviewed"} for fid in families],
        "rights": "user_assertion_only_not_owner_authorization",
        "mode_options": ["reference", "snapshot"],
        "note": "Select the real content family before ingestion. For CSV accounting use kind=acomba with declared record-type; for bibliographic JSON use kind=bibliography. These are suggestions only.",
    }
