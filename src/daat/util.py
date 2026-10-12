"""Stable utilities for local reports (not Kristal's JCS identity hashing)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any
from .errors import ContractError

def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_bytes(obj: Any) -> bytes:
    # Local request de-duplication only. NOT the Kristal/JCS wire algorithm.
    return json.dumps(obj,sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False).encode('utf-8')

def json_digest(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def load_json(path: Path, max_bytes: int=1_048_576) -> Any:
    if not path.is_file() or path.stat().st_size > max_bytes:
        raise ContractError('INPUT_SIZE','JSON missing or exceeds allowed size')
    try:
        return json.loads(path.read_text(encoding='utf-8'),parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (UnicodeError,ValueError) as e:
        raise ContractError('JSON_INVALID','Invalid UTF-8 JSON') from e

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
