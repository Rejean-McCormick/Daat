"""Strict static adapter declarations, handler registration and lane routing.

Registry cannot load Python modules or execute untrusted manifest code. External
workers must be explicitly injected by an authenticated, approved host.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from importlib.resources import files
from typing import Any, Callable, Protocol

from jsonschema import Draft202012Validator

from .catalog import source_family
from .errors import AdmissionError
from .source import ReadLimits, SourceSelection, Evidence
from .util import json_digest, load_json


class ReaderPort(Protocol):
    def __call__(self, selection: SourceSelection) -> tuple[list[Evidence], str, list[str], str | None]: ...


def _manifest_schema() -> dict[str, Any]:
    from json import loads
    return loads(files("daat").joinpath("resources", "contracts", "daat", "adapter-manifest.schema.json").read_text(encoding="utf-8"))


def validate_adapter_manifest(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise AdmissionError("ADAPTER_MANIFEST_INVALID", "Adapter manifest must be an object")
    errors = list(Draft202012Validator(_manifest_schema()).iter_errors(raw))
    if errors:
        raise AdmissionError("ADAPTER_MANIFEST_INVALID", sorted(errors, key=lambda e: e.message)[0].message)
    for family_id in raw["family_ids"]:
        source_family(family_id)
    return dict(raw)


def read_adapter_manifest(path: Path) -> dict[str, Any]:
    return validate_adapter_manifest(load_json(path, max_bytes=65536))


def _declare(adapter: str, kind: str, lane: str, families: tuple[str, ...], description: str) -> dict[str, Any]:
    return validate_adapter_manifest({
        "format": "daat.local-adapter/0.1.0-prototype",
        "id": adapter, "version": "0.4.0", "kind": kind, "lane": lane,
        "family_ids": list(families), "read_only": True,
        "implementation": "built_in", "source_rights_required": True,
        "description": description, "approved_owner_profile": None,
    })


def _pdf(s: SourceSelection):
    from .connectors.pdf import read_pdf
    rows, digest = read_pdf(s.path(), s.limits, s.relative_path)
    return rows, digest, [], None


def _archive(s: SourceSelection):
    from .connectors.archive import read_archive
    rows, digest = read_archive(s.path(), s.limits, s.relative_path)
    return rows, digest, [], None


def _dataset(s: SourceSelection):
    from .connectors.common import read_dataset
    rows, digest = read_dataset(s.path(), s.limits, s.relative_path)
    return rows, digest, [], None


def _git(s: SourceSelection):
    from .connectors.git import read_git
    return read_git(s.path(), s.revision, s.limits, s.relative_path)


def _bibliography(s: SourceSelection):
    from .connectors.bibliography import read_bibliography
    rows, digest, warnings = read_bibliography(s.path(), s.limits, s.relative_path)
    return rows, digest, warnings, None


def _acomba(s: SourceSelection):
    from .connectors.acomba import read_acomba
    rows, digest, warnings = read_acomba(s.path(), s.limits, s.relative_path, s.record_type)
    return rows, digest, warnings, None


class AdapterRegistry:
    """Portable local mapping of explicit adapter manifests to trusted callables."""
    def __init__(self) -> None:
        self._items: dict[str, tuple[dict[str, Any], ReaderPort]] = {}

    def register(self, manifest: dict[str, Any], reader: ReaderPort, *, trusted_host: bool = False) -> None:
        item = validate_adapter_manifest(manifest)
        if item["implementation"] == "trusted_host_worker" and not trusted_host:
            raise AdmissionError("ADAPTER_UNTRUSTED", "Worker must be registered by trusted operator host")
        if item["id"] in self._items or any(m["kind"] == item["kind"] for m, _ in self._items.values()):
            raise AdmissionError("ADAPTER_DUPLICATE", "Adapter ID or kind already registered")
        if not callable(reader):
            raise AdmissionError("ADAPTER_INVALID", "Explicit reader callable required")
        self._items[item["id"]] = (item, reader)

    def list(self) -> list[dict[str, Any]]:
        return [dict(item, implementation_status="offline_local_reader_not_owner_integrated")
                for item, _ in sorted(self._items.values(), key=lambda pair: pair[0]["id"])]

    def resolve(self, selection: SourceSelection) -> tuple[dict[str, Any], ReaderPort]:
        source_family(selection.family_id)
        options = [(a, h) for a, h in self._items.values()
                   if a["kind"] == selection.kind and selection.family_id in a["family_ids"]]
        if len(options) != 1:
            raise AdmissionError("ADAPTER_UNAVAILABLE", "No declared read-only adapter for this kind/family")
        if selection.mode == "sync-preview":
            raise AdmissionError("SOURCE_MODE_UNSUPPORTED", "Continuous sync requires owner-approved runtime")
        return options[0]


def builtin_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    items = (
        (_declare("local.pdf", "pdf", "L1", ("02", "08", "09", "20", "21", "22", "28"),
                  "Bounded PDF extraction using optional local pypdf without OCR or remote fetching"), _pdf),
        (_declare("local.zip", "archive", "L1", ("08", "09", "28"),
                  "Bounded ZIP archive preview without unpacking or nested archives"), _archive),
        (_declare("local.tabular", "dataset", "L1", ("07", "16", "17", "26", "30", "32"),
                  "Local CSV TSV JSON JSONL record extraction with stable row anchors"), _dataset),
        (_declare("local.git", "git", "L5", ("11", "12"),
                  "Pinned Git snapshot reader without checkout or execution"), _git),
        (_declare("local.bibliography", "bibliography", "L1", ("01", "02", "03"),
                  "Local licensed bibliography metadata from JSON JSONL CSV RIS or XML"), _bibliography),
        (_declare("local.acomba", "acomba", "L1", ("13", "14"),
                  "Local read-only typed accounting export without SDK or ODBC"), _acomba),
    )
    for item, reader in items:
        registry.register(item, reader)
    return registry
