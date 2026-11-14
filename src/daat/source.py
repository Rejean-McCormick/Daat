"""Local, noncanonical source evidence for DaaT's offline onramp.

These objects deliberately are NOT IK envelopes, Kristal states, source custody
receipts or evidence of authorization by an external owner. They are typed local
preview artifacts. No permanent source database is maintained here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import re
from typing import Any, Mapping

from .errors import AdmissionError
from .util import json_digest

_IDENTIFIER = re.compile(r"^[a-zA-Z0-9_.:/-]{2,128}$")
_HEX = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_MODES = frozenset({"snapshot", "reference", "sync-preview"})
_ALLOWED_CLASSES = frozenset({"public", "internal", "confidential", "restricted"})


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bounded_file_digest(path: Path, *, max_bytes: int) -> str:
    """Hash a bounded local regular file without retaining its bytes in RAM."""
    if not path.is_file() or path.is_symlink():
        raise AdmissionError("SOURCE_UNSAFE", "Source is not a regular non-symlink file")
    size = path.stat().st_size
    if size < 0 or size > max_bytes:
        raise AdmissionError("SOURCE_LIMIT", "Source exceeds the declared byte limit")
    result = hashlib.sha256()
    consumed = 0
    with path.open("rb") as stream:
        while True:
            part = stream.read(min(65536, max_bytes - consumed + 1))
            if not part:
                break
            consumed += len(part)
            if consumed > max_bytes:
                raise AdmissionError("SOURCE_LIMIT", "Source changed beyond byte limit")
            result.update(part)
    return result.hexdigest()


def confined_path(root: Path, name: str, *, allow_directory: bool = False) -> Path:
    """Permit only paths below an explicitly selected local root; deny symlinks.

    This rejects known symlinks but is not an OS-level race-free sandbox. An
    approved execution host must isolate attacker-writable roots in production.
    """
    root = Path(root).absolute()
    if not root.is_dir() or root.is_symlink():
        raise AdmissionError("SOURCE_ROOT_INVALID", "An actual, non-symlink directory root is required")
    if not isinstance(name, str) or not name or "\x00" in name or name.startswith("\\") or name.startswith("//"):
        raise AdmissionError("SOURCE_PATH_INVALID", "Invalid source name")
    path = Path(name)
    if path.is_absolute() or any(part in ("..", "") for part in path.parts):
        raise AdmissionError("SOURCE_PATH_INVALID", "Source path must be relative and bounded")
    pointer = root
    for segment in path.parts:
        pointer = pointer / segment
        if pointer.is_symlink():
            raise AdmissionError("SOURCE_UNSAFE", "Symlink traversal is forbidden")
    resolved = pointer.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise AdmissionError("SOURCE_PATH_INVALID", "Source escapes the selected root")
    if not resolved.exists() or (not (resolved.is_dir() or resolved.is_file()) if allow_directory else not resolved.is_file()):
        raise AdmissionError("SOURCE_NOT_FOUND", "Selected source is absent or of the wrong type")
    return resolved


@dataclass(frozen=True)
class ReadLimits:
    max_source_bytes: int = 20_000_000
    max_records: int = 500
    max_text_chars: int = 30_000
    max_files: int = 500
    max_archive_ratio: int = 50

    def __post_init__(self) -> None:
        values = (self.max_source_bytes, self.max_records, self.max_text_chars, self.max_files, self.max_archive_ratio)
        if any(type(x) is not int or x <= 0 for x in values):
            raise AdmissionError("SOURCE_LIMIT_INVALID", "All read limits must be positive integers")
        if self.max_source_bytes > 500_000_000 or self.max_records > 10000 or self.max_files > 10000:
            raise AdmissionError("SOURCE_LIMIT_INVALID", "Configured offline upper limit exceeded")


@dataclass(frozen=True)
class RightsDeclaration:
    tenant: str
    purpose: str
    license: str
    asserted_by: str
    permission_asserted: bool = False
    classification: str = "internal"
    redistributable: bool = False
    valid_until: str | None = None

    def __post_init__(self) -> None:
        if any(not isinstance(x, str) or not _IDENTIFIER.fullmatch(x) for x in (self.tenant, self.asserted_by)):
            raise AdmissionError("RIGHTS_INVALID", "Tenant and asserted_by must be explicit bounded identifiers")
        if type(self.permission_asserted) is not bool or type(self.redistributable) is not bool:
            raise AdmissionError("RIGHTS_INVALID", "Permission and distribution flags must be booleans")
        if not self.permission_asserted:
            raise AdmissionError("RIGHTS_NOT_ASSERTED", "Explicit read/use rights acknowledgement is mandatory")
        if not self.purpose.strip() or len(self.purpose) > 250 or not self.license.strip() or len(self.license) > 250:
            raise AdmissionError("RIGHTS_INVALID", "Purpose and source license/terms must be supplied")
        if self.classification not in _ALLOWED_CLASSES:
            raise AdmissionError("RIGHTS_INVALID", "Unsupported source classification")
        if self.valid_until is not None:
            if not isinstance(self.valid_until, str):
                raise AdmissionError("RIGHTS_INVALID", "Grant expiry must be a timestamp string")
            try:
                until = datetime.fromisoformat(self.valid_until.replace("Z", "+00:00"))
            except ValueError as exc:
                raise AdmissionError("RIGHTS_INVALID", "Invalid grant expiry") from exc
            if until.tzinfo is None or until <= datetime.now(timezone.utc):
                raise AdmissionError("RIGHTS_EXPIRED", "Source right declaration has expired or is timezone-naive")

    def public_metadata(self) -> dict[str, Any]:
        """No proof is asserted: local user declaration only."""
        return {
            "tenant": self.tenant, "purpose": self.purpose,
            "license_or_terms": self.license, "asserted_by": self.asserted_by,
            "verification": "user_assertion_only_not_owner_authorization",
            "classification": self.classification,
            "redistributable": self.redistributable,
            "valid_until": self.valid_until,
        }


@dataclass(frozen=True)
class SourceSelection:
    root: Path
    relative_path: str
    kind: str
    family_id: str
    rights: RightsDeclaration
    mode: str = "snapshot"
    record_type: str | None = None
    revision: str | None = None
    limits: ReadLimits = field(default_factory=ReadLimits)

    def __post_init__(self) -> None:
        if self.mode not in _ALLOWED_MODES:
            raise AdmissionError("SOURCE_MODE_UNSUPPORTED", "Unknown local source mode")
        if not re.fullmatch(r"[0-9]{2}", self.family_id):
            raise AdmissionError("SOURCE_FAMILY_INVALID", "Source family must be a catalogue ID")
        if self.record_type is not None and (not re.fullmatch(r"[a-z][a-z0-9_-]{1,63}", self.record_type)):
            raise AdmissionError("SOURCE_RECORD_TYPE_INVALID", "Invalid declared record type")
        if self.revision is not None and (not isinstance(self.revision, str) or len(self.revision) > 100):
            raise AdmissionError("SOURCE_REVISION_INVALID", "Invalid revision")

    def path(self) -> Path:
        return confined_path(self.root, self.relative_path, allow_directory=(self.kind == "git"))


@dataclass(frozen=True)
class Evidence:
    anchor_kind: str
    location: str
    source_sha256: str
    data: Mapping[str, Any]
    record_type: str
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        if not _HEX.fullmatch(self.source_sha256):
            raise AdmissionError("EVIDENCE_INVALID", "Missing source byte digest")
        if not self.anchor_kind or not self.location or len(self.location) > 1024:
            raise AdmissionError("EVIDENCE_INVALID", "Source anchor required")
        if not isinstance(self.data, Mapping):
            raise AdmissionError("EVIDENCE_INVALID", "Evidence data must be a mapping")
        body = {
            "anchor": {"kind": self.anchor_kind, "location": self.location},
            "source_sha256": self.source_sha256,
            "record_type": self.record_type,
            "data": dict(self.data),
            "warnings": list(self.warnings),
        }
        body["local_evidence_id"] = "ev-" + json_digest(body)
        return body


def make_preparation(selection: SourceSelection, *, adapter_id: str, adapter_version: str,
                     records: list[Evidence], source_digest: str, warnings: list[str] | None = None,
                     source_revision: str | None = None) -> dict[str, Any]:
    """Content-addressed, noncanonical local preview, without invented owner receipts."""
    if not _HEX.fullmatch(source_digest):
        raise AdmissionError("EVIDENCE_INVALID", "Source manifest digest missing")
    if len(records) > selection.limits.max_records:
        raise AdmissionError("SOURCE_LIMIT", "Record count over limit")
    data = {
        "format": "daat.local-evidence-preview/0.1.0-prototype",
        "authority": "noncanonical_unreviewed",
        "owner_handoff": "blocked_pending_owner_adopted_contract",
        "source": {
            "kind": selection.kind, "family_id": selection.family_id,
            "local_ref": selection.relative_path.replace("\\", "/"),
            "revision": source_revision or selection.revision,
            "manifest_sha256": source_digest,
            "rights": selection.rights.public_metadata(),
        },
        "extraction": {"adapter_id": adapter_id, "adapter_version": adapter_version,
                       "deterministic": True, "executed_external_code": False},
        "records": [record.as_dict() for record in records],
        "warnings": list(warnings or []),
    }
    data["preview_sha256"] = json_digest(data)
    return data
