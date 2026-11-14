"""Bounded atomic private local preview serialization (not source custody)."""
from __future__ import annotations
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from .errors import AdmissionError
from .util import canonical_bytes


def write_private_json(path: Path, obj: Any, *, replace: bool = False) -> None:
    path = Path(path)
    parent = path.parent.absolute()
    if not parent.is_dir() or parent.is_symlink() or path.is_symlink():
        raise AdmissionError("OUTPUT_PATH_UNSAFE", "Output must be inside an existing non-symlink directory")
    if path.exists() and not replace:
        raise AdmissionError("OUTPUT_EXISTS", "Output already exists; explicit --replace required")
    raw = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True, allow_nan=False).encode("utf-8") + b"\n"
    if len(raw) > 100_000_000:
        raise AdmissionError("OUTPUT_LIMIT", "Preview output exceeds 100 MB")
    name: str | None = None
    try:
        fd, name = tempfile.mkstemp(prefix=".daat-private-", suffix=".json", dir=str(parent))
        with os.fdopen(fd, "wb") as stream:
            os.chmod(name, 0o600)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if path.is_symlink() or (path.exists() and not replace):
            raise AdmissionError("OUTPUT_PATH_UNSAFE", "Output target changed during write")
        os.replace(name, path)
        name = None
    finally:
        if name and os.path.exists(name):
            os.unlink(name)
