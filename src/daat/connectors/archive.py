"""ZIP archive evidence preview: no extraction to disk or nested archives."""
from __future__ import annotations
from io import BytesIO
from pathlib import Path, PurePosixPath
import stat
import zipfile

from ..errors import AdmissionError
from ..source import Evidence, ReadLimits, digest_bytes
from .common import read_bounded, read_dataset_bytes, decode_utf8
from .pdf import read_pdf_bytes

_ACCEPTED = {".pdf", ".csv", ".tsv", ".jsonl", ".json", ".txt", ".md"}


def read_archive(path: Path, limits: ReadLimits, label: str) -> tuple[list[Evidence], str]:
    blob = read_bounded(path, limits)
    digest = digest_bytes(blob)
    result: list[Evidence] = []
    total = 0
    seen = set()
    try:
        with zipfile.ZipFile(BytesIO(blob), "r") as archive:
            members = archive.infolist()
            if len(members) > limits.max_files:
                raise AdmissionError("SOURCE_LIMIT", "Archive has too many members")
            for member in members:
                if member.flag_bits & 1:
                    raise AdmissionError("SOURCE_ARCHIVE_INVALID", "Encrypted ZIP member requires separately approved reader")
                if member.is_dir():
                    continue
                name = member.filename
                part = PurePosixPath(name)
                if name.startswith("/") or "\\" in name or any(x in ("..", "") for x in part.parts) or name in seen:
                    raise AdmissionError("SOURCE_ARCHIVE_INVALID", "Invalid or duplicate ZIP entry path")
                seen.add(name)
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise AdmissionError("SOURCE_ARCHIVE_INVALID", "Archive symlinks are not allowed")
                suffix = part.suffix.lower()
                if suffix not in _ACCEPTED:
                    raise AdmissionError("SOURCE_ARCHIVE_UNSUPPORTED", "Archive contains unsupported or nested format")
                total += member.file_size
                if member.file_size > limits.max_source_bytes or total > limits.max_source_bytes:
                    raise AdmissionError("SOURCE_LIMIT", "Archive uncompressed byte limit exceeded")
                if member.file_size > limits.max_archive_ratio * max(1, member.compress_size):
                    raise AdmissionError("SOURCE_ARCHIVE_BOMB", "Archive compression ratio too high")
                with archive.open(member) as fh:
                    data = fh.read(member.file_size + 1)
                if len(data) != member.file_size:
                    raise AdmissionError("SOURCE_ARCHIVE_INVALID", "ZIP member size changed")
                anchor = label + "!" + name
                if suffix == ".pdf":
                    records, _ = read_pdf_bytes(data, limits, anchor)
                elif suffix in (".txt", ".md"):
                    text = decode_utf8(data)
                    if len(text) > limits.max_text_chars:
                        raise AdmissionError("SOURCE_LIMIT", "Archive text item too large")
                    records = [Evidence("archive_entry", anchor, digest_bytes(data),
                                        {"text": text}, "document_text")]
                else:
                    records, _ = read_dataset_bytes(data, suffix, limits, anchor)
                if len(result) + len(records) > limits.max_records:
                    raise AdmissionError("SOURCE_LIMIT", "Archive record limit exceeded")
                result.extend(records)
    except (zipfile.BadZipFile, EOFError, OSError) as exc:
        raise AdmissionError("SOURCE_ARCHIVE_INVALID", "Corrupted ZIP archive") from exc
    return result, digest
