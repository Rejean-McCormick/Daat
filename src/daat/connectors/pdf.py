"""PDF proof-of-concept with page anchors and optional independently installed pypdf.

No external OCR or web/model downloads. In production untrusted PDFs require
OS/container parser isolation; an in-process Python reader alone is not a sandbox.
"""
from __future__ import annotations
from io import BytesIO
from pathlib import Path
from typing import Any
from ..errors import AdmissionError
from ..source import Evidence, ReadLimits, digest_bytes
from .common import read_bounded


def read_pdf_bytes(blob: bytes, limits: ReadLimits, label: str) -> tuple[list[Evidence], str]:
    if len(blob) > limits.max_source_bytes or not blob.startswith(b"%PDF-"):
        raise AdmissionError("SOURCE_PDF_INVALID", "PDF magic bytes missing or source oversized")
    sha = digest_bytes(blob)
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise AdmissionError("DEPENDENCY_MISSING", "PDF extraction needs optional `pypdf` extra (no download performed)") from exc
    try:
        reader = PdfReader(BytesIO(blob), strict=True)
        if reader.is_encrypted:
            raise AdmissionError("SOURCE_PDF_ENCRYPTED", "Encrypted PDF requires a separately approved reader")
        if len(reader.pages) > limits.max_records:
            raise AdmissionError("SOURCE_LIMIT", "PDF page count beyond configured maximum")
        records: list[Evidence] = []
        for index, page in enumerate(reader.pages, 1):
            content = page.extract_text() or ""
            if len(content) > limits.max_text_chars:
                raise AdmissionError("SOURCE_LIMIT", "Extracted PDF page over text size limit")
            records.append(Evidence("pdf_page", f"{label}#page:{index}", sha,
                                    {"text": content, "page": index}, "document_page",
                                    ("no_extractable_text",) if not content.strip() else ()))
        return records, sha
    except AdmissionError:
        raise
    except Exception as exc:
        raise AdmissionError("SOURCE_PDF_INVALID", "PDF parser rejected source") from exc


def read_pdf(path: Path, limits: ReadLimits, label: str) -> tuple[list[Evidence], str]:
    return read_pdf_bytes(read_bounded(path, limits), limits, label)
