"""Licensed local scholarly metadata previews (not provider harvesting)."""
from __future__ import annotations
import re
from pathlib import Path
from xml.etree import ElementTree
from typing import Any

from ..errors import AdmissionError
from ..source import Evidence, ReadLimits, digest_bytes
from .common import read_bounded, decode_utf8, json_strict, parse_tabular

_DOI = re.compile(r"^10\.\d{4,9}/[^\s]+$", re.I)


def _norm_record(item: dict[str, Any]) -> dict[str, Any]:
    if "DOI" in item and "doi" not in item:
        item = dict(item, doi=item["DOI"])
    if "doi" in item and item["doi"] not in ("", None):
        doi = item["doi"]
        if not isinstance(doi, str):
            raise AdmissionError("SOURCE_BIBLIO_INVALID", "DOI must be a string")
        doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi.strip(), flags=re.I)
        if not _DOI.fullmatch(doi):
            raise AdmissionError("SOURCE_BIBLIO_INVALID", "DOI format invalid; not auto-reconciled")
        item = dict(item, doi=doi.lower())
    return item


def _ris_records(text: str, limits: ReadLimits) -> list[tuple[str, dict[str, Any]]]:
    result: list[tuple[str, dict[str, Any]]] = []
    item: dict[str, Any] = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if len(line) < 6 or line[2:6] != "  - " or not line[:2].isupper():
            raise AdmissionError("SOURCE_BIBLIO_INVALID", "Invalid RIS tag line")
        tag, value = line[:2], line[6:]
        if len(value) > limits.max_text_chars:
            raise AdmissionError("SOURCE_LIMIT", "RIS field too long")
        if tag == "TY" and item:
            raise AdmissionError("SOURCE_BIBLIO_INVALID", "Missing end-of-record marker")
        if tag == "ER":
            if not item:
                raise AdmissionError("SOURCE_BIBLIO_INVALID", "RIS end marker without record")
            result.append((f"ris_record:{len(result)+1}", item))
            item = {}
        else:
            if tag in item:
                old = item[tag]
                item[tag] = (old if isinstance(old, list) else [old]) + [value]
            else:
                item[tag] = value
        if len(result) > limits.max_records:
            raise AdmissionError("SOURCE_LIMIT", "RIS record limit exceeded")
    if item:
        raise AdmissionError("SOURCE_BIBLIO_INVALID", "Incomplete RIS last record")
    return result


def _xml_records(blob: bytes, limits: ReadLimits) -> list[tuple[str, dict[str, Any]]]:
    # Reject any XML entities/DTD, rather than accept ambiguous parser behavior.
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)", blob, re.I):
        raise AdmissionError("SOURCE_XML_UNSAFE", "DTD and XML entities are forbidden")
    try:
        root = ElementTree.fromstring(blob)
    except ElementTree.ParseError as exc:
        raise AdmissionError("SOURCE_XML_INVALID", "XML parser rejected scholarly metadata") from exc
    def local(tag: str) -> str:
        return tag.rsplit("}", 1)[-1]
    records: list[tuple[str, dict[str, Any]]] = []
    for element in root.iter():
        if local(element.tag) not in ("record", "entry", "article"):
            continue
        record: dict[str, Any] = {}
        for node in element.iter():
            typ = local(node.tag)
            if typ not in ("title", "identifier", "creator", "date", "publisher", "type", "description", "subject"):
                continue
            value = (node.text or "").strip()
            if not value:
                continue
            if len(value) > limits.max_text_chars:
                raise AdmissionError("SOURCE_LIMIT", "Scholarly XML field oversized")
            record.setdefault(typ, []).append(value)
        if record:
            records.append((f"xml_record:{len(records)+1}", record))
            if len(records) > limits.max_records:
                raise AdmissionError("SOURCE_LIMIT", "Scholarly XML record cap reached")
    return records


def read_bibliography(path: Path, limits: ReadLimits, label: str) -> tuple[list[Evidence], str, list[str]]:
    blob = read_bounded(path, limits)
    sha = digest_bytes(blob)
    suffix = path.suffix.lower()
    if suffix in (".csv", ".tsv", ".jsonl"):
        items = parse_tabular(blob, suffix, limits)
    elif suffix == ".json":
        obj = json_strict(decode_utf8(blob))
        if isinstance(obj, dict):
            obj = obj.get("message", obj)
            if isinstance(obj, dict):
                obj = obj.get("items", obj.get("records", [obj]))
        if not isinstance(obj, list) or len(obj) > limits.max_records:
            raise AdmissionError("SOURCE_BIBLIO_INVALID", "Invalid bounded bibliographic JSON list")
        items = [(f"item:{i}", entry) for i, entry in enumerate(obj)]
    elif suffix == ".ris":
        items = _ris_records(decode_utf8(blob), limits)
    elif suffix == ".xml":
        items = _xml_records(blob, limits)
    else:
        raise AdmissionError("SOURCE_FORMAT_UNSUPPORTED", "Unsupported bibliography format")
    records: list[Evidence] = []
    identifiers: dict[str, list[str]] = {}
    for locator, item in items:
        if not isinstance(item, dict):
            raise AdmissionError("SOURCE_BIBLIO_INVALID", "Metadata record must be object")
        norm = _norm_record(item)
        doi = norm.get("doi")
        if isinstance(doi, str) and doi:
            identifiers.setdefault(doi, []).append(locator)
        records.append(Evidence("bibliographic_record", f"{label}#{locator}", sha,
                                norm, "scholarly_metadata_unvalidated"))
    warnings = ["possible_duplicate_doi:" + d for d, locations in identifiers.items() if len(locations) > 1]
    return records, sha, warnings
