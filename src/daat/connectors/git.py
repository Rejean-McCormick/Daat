"""Read-only pinned Git commit reader; never checks out, fetches or runs repo code.

Uses only `rev-parse`, `ls-tree`, `cat-file`, which do not run hooks, build tools,
filters or submodules. All content remains an untrusted user-supplied claim.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

from ..errors import AdmissionError
from ..source import Evidence, ReadLimits, digest_bytes
from ..util import json_digest

_COMMIT = re.compile(r"^[a-fA-F0-9]{40}(?:[a-fA-F0-9]{24})?$")
_ALLOWED_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".rst", ".txt", ".json", ".jsonl",
                     ".yaml", ".yml", ".toml", ".xml", ".csv", ".go", ".rs", ".java", ".c", ".h",
                     ".cpp", ".cs", ".sql", ".sh", ".ps1", ".rb", ".html", ".css", ".tex"}
_EXCLUDED_SEGMENTS = {".git", "node_modules", "vendor", "dist", "build", "__pycache__", ".venv", "venv",
                      "target", "coverage", ".next"}
_EXCLUDED_NAMES = {".env", ".npmrc", ".netrc", ".pypirc", "id_rsa", "id_ed25519", ".git-credentials"}
_SECRET_PATTERNS = (re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----", re.I),
                    re.compile(r"\b(?:ghp_|github_pat_|glpat-)[a-zA-Z0-9_]{12,}"),
                    re.compile(r"\bAKIA[A-Z0-9]{16}\b"))


def _git(repo: Path, args: list[str], *, limit: int = 2_000_000) -> bytes:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("PYTHONPATH", "LD_PRELOAD")}
    env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_NO_REPLACE_OBJECTS": "1", "GIT_NO_LAZY_FETCH": "1",
                "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"})
    try:
        process = subprocess.Popen(["git", "-C", str(repo), "-c", "core.hooksPath=" + os.devnull,
                                    *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)
        assert process.stdout is not None
        try:
            content = process.stdout.read(limit + 1)
            if len(content) > limit:
                process.kill()
                process.wait(timeout=4)
                raise AdmissionError("SOURCE_LIMIT", "Git command output over the bounded limit")
            code = process.wait(timeout=12)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            process.wait(timeout=4)
            raise AdmissionError("SOURCE_TIMEOUT", "Local Git operation timed out") from exc
        if code != 0:
            raise AdmissionError("SOURCE_GIT_INVALID", "Git command rejected the selected repository/revision")
        return content
    except FileNotFoundError as exc:
        raise AdmissionError("DEPENDENCY_MISSING", "Git executable is not installed") from exc


def _object_matches(blob: bytes, object_id: str) -> bool:
    payload = b"blob " + str(len(blob)).encode("ascii") + b"\x00" + blob
    algorithm = hashlib.sha1 if len(object_id) == 40 else hashlib.sha256
    return algorithm(payload).hexdigest() == object_id.lower()


def read_git(repo: Path, commit: str | None, limits: ReadLimits, label: str) -> tuple[list[Evidence], str, list[str], str]:
    if commit is None or not _COMMIT.fullmatch(commit):
        raise AdmissionError("SOURCE_GIT_UNPINNED", "An immutable full 40/64-hex commit is required")
    if not (repo / ".git").is_dir() or (repo / ".git").is_symlink():
        raise AdmissionError("SOURCE_GIT_INVALID", "Only a local normal Git checkout is supported")
    pinned = _git(repo, ["rev-parse", "--verify", commit + "^{commit}"], limit=128).decode("ascii").strip().lower()
    if pinned != commit.lower():
        raise AdmissionError("SOURCE_GIT_UNPINNED", "Revision must be an exact commit object ID")
    tree = _git(repo, ["ls-tree", "-rz", "--full-tree", pinned], limit=min(limits.max_source_bytes, 8_000_000))
    entries = tree.split(b"\x00")
    if entries[-1] == b"":
        entries.pop()
    if len(entries) > limits.max_files:
        raise AdmissionError("SOURCE_LIMIT", "Git tree has too many paths (select a smaller repository)")
    records: list[Evidence] = []
    warnings: list[str] = []
    included: list[tuple[str, str, str]] = []
    consumed = 0
    for entry in entries:
        try:
            meta, rawpath = entry.split(b"\t", 1)
            mode, kind, object_id_bytes = meta.decode("ascii").split(" ")
            relpath = rawpath.decode("utf-8", errors="strict")
        except (ValueError, UnicodeError) as exc:
            raise AdmissionError("SOURCE_GIT_INVALID", "Invalid Git tree entry") from exc
        path = PurePosixPath(relpath)
        if (path.is_absolute() or ".." in path.parts or "\\" in relpath or not path.parts or
                ".git" in path.parts):
            raise AdmissionError("SOURCE_GIT_INVALID", "Unsafe source path in tree")
        if mode not in ("100644", "100755") or kind != "blob":
            warnings.append("skipped_nonregular_git_entry:" + relpath)
            continue
        if (any(s in _EXCLUDED_SEGMENTS for s in path.parts) or
                path.name in _EXCLUDED_NAMES or path.suffix.lower() not in _ALLOWED_SUFFIXES or
                path.name.lower().endswith((".key", ".pem", ".p12", ".pfx"))):
            warnings.append("skipped_disallowed_git_entry:" + relpath)
            continue
        object_id = object_id_bytes.lower()
        if not _COMMIT.fullmatch(object_id):
            raise AdmissionError("SOURCE_GIT_INVALID", "Unexpected Git object ID")
        size_raw = _git(repo, ["cat-file", "-s", object_id], limit=64).decode("ascii").strip()
        if not size_raw.isdigit():
            raise AdmissionError("SOURCE_GIT_INVALID", "Invalid Git object size")
        size = int(size_raw)
        if size > limits.max_text_chars * 4 or consumed + size > limits.max_source_bytes:
            warnings.append("skipped_oversized_git_entry:" + relpath)
            continue
        blob = _git(repo, ["cat-file", "blob", object_id], limit=size)
        if len(blob) != size or not _object_matches(blob, object_id):
            raise AdmissionError("SOURCE_INTEGRITY", "Git blob digest/size mismatch")
        consumed += size
        try:
            content = blob.decode("utf-8-sig")
        except UnicodeDecodeError:
            warnings.append("skipped_nonutf8_git_entry:" + relpath)
            continue
        if "\x00" in content or len(content) > limits.max_text_chars:
            warnings.append("skipped_binary_or_long_git_entry:" + relpath)
            continue
        if any(regex.search(content) for regex in _SECRET_PATTERNS):
            warnings.append("skipped_possible_secret_git_entry:" + relpath)
            continue
        checksum = digest_bytes(blob)
        records.append(Evidence("git_blob", f"{label}@{pinned}:{relpath}#{object_id}", checksum,
                                {"path": relpath, "blob_id": object_id, "commit": pinned, "text": content},
                                "repository_blob"))
        included.append((relpath, object_id, checksum))
        if len(records) > limits.max_records:
            raise AdmissionError("SOURCE_LIMIT", "Git record count over limit")
    return records, json_digest({"commit": pinned, "selected_blobs": included}), warnings, pinned
