"""Common safe parsers for bounded, locally authorized artifacts."""
from __future__ import annotations

import csv
import io
import json
import math
from pathlib import Path
from typing import Any, Iterator

from ..errors import AdmissionError
from ..source import Evidence, ReadLimits, bounded_file_digest, digest_bytes


def read_bounded(path: Path, limits: ReadLimits) -> bytes:
    if path.stat().st_size > limits.max_source_bytes:
        raise AdmissionError("SOURCE_LIMIT", "Local file exceeds maximum bytes")
    with path.open("rb") as handle:
        data = handle.read(limits.max_source_bytes + 1)
    if len(data) > limits.max_source_bytes:
        raise AdmissionError("SOURCE_LIMIT", "Local file read exceeded maximum bytes")
    return data


def decode_utf8(blob: bytes) -> str:
    try:
        text = blob.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise AdmissionError("SOURCE_ENCODING", "Only UTF-8 text is supported by this reader") from exc
    if "\x00" in text:
        raise AdmissionError("SOURCE_ENCODING", "Binary content rejected by text reader")
    return text


def json_strict(text: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict:
        value: dict[str, Any] = {}
        for key, v in items:
            if key in value:
                raise AdmissionError("SOURCE_DUPLICATE_FIELD", "JSON key repeated")
            value[key] = v
        return value

    try:
        return json.loads(text, object_pairs_hook=pairs,
                          parse_float=lambda number: _finite_float(number),
                          parse_constant=lambda c: (_ for _ in ()).throw(ValueError("Nonfinite JSON number")))
    except (ValueError, RecursionError) as exc:
        raise AdmissionError("SOURCE_JSON_INVALID", "Invalid JSON document") from exc


def parse_tabular(blob: bytes, suffix: str, limits: ReadLimits) -> list[tuple[str, dict[str, Any]]]:
    text = decode_utf8(blob)
    rows: list[tuple[str, dict[str, Any]]] = []
    if suffix in (".csv", ".tsv"):
        reader = csv.DictReader(io.StringIO(text, newline=""), delimiter="\t" if suffix == ".tsv" else ",")
        names = reader.fieldnames
        if not names or len(set(names)) != len(names) or any(not n or len(n) > 128 for n in names):
            raise AdmissionError("SOURCE_CSV_INVALID", "Missing, duplicate or oversized CSV headers")
        for i, row in enumerate(reader, 2):
            if len(rows) >= limits.max_records:
                raise AdmissionError("SOURCE_LIMIT", "CSV record cap reached")
            if None in row or any(value is None for value in row.values()):
                raise AdmissionError("SOURCE_CSV_INVALID", "CSV row shape does not match headers")
            if any(len(str(v)) > limits.max_text_chars for v in row.values()):
                raise AdmissionError("SOURCE_LIMIT", "CSV field over size limit")
            rows.append((f"row:{i}", row))
    elif suffix == ".jsonl":
        for i, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            if len(rows) >= limits.max_records:
                raise AdmissionError("SOURCE_LIMIT", "JSONL record cap reached")
            if len(line) > limits.max_text_chars * 20:
                raise AdmissionError("SOURCE_LIMIT", "JSONL row too large")
            obj = json_strict(line)
            if not isinstance(obj, dict):
                raise AdmissionError("SOURCE_JSON_INVALID", "JSONL rows must be objects")
            rows.append((f"line:{i}", obj))
    elif suffix == ".json":
        obj = json_strict(text)
        if isinstance(obj, dict) and isinstance(obj.get("records"), list):
            obj = obj["records"]
        if not isinstance(obj, list):
            raise AdmissionError("SOURCE_JSON_INVALID", "Expected JSON array or object with records array")
        if len(obj) > limits.max_records:
            raise AdmissionError("SOURCE_LIMIT", "JSON record cap reached")
        for i, entry in enumerate(obj):
            if not isinstance(entry, dict):
                raise AdmissionError("SOURCE_JSON_INVALID", "JSON entries must be objects")
            rows.append((f"item:{i}", entry))
    else:
        raise AdmissionError("SOURCE_FORMAT_UNSUPPORTED", "Unsupported tabular file suffix")
    return rows


def read_dataset_bytes(blob: bytes, suffix: str, limits: ReadLimits, label: str) -> tuple[list[Evidence], str]:
    if len(blob) > limits.max_source_bytes:
        raise AdmissionError("SOURCE_LIMIT", "Content exceeds byte limit")
    checksum = digest_bytes(blob)
    rows = parse_tabular(blob, suffix, limits)
    records = [Evidence("record", f"{label}#{locator}", checksum, data, "source_record")
               for locator, data in rows]
    return records, checksum


def read_dataset(path: Path, limits: ReadLimits, label: str) -> tuple[list[Evidence], str]:
    blob = read_bounded(path, limits)
    return read_dataset_bytes(blob, path.suffix.lower(), limits, label)


def _finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Nonfinite JSON exponent")
    return result
