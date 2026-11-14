"""Local crash-resumable *preview* metadata journal; not a domain outbox or IK bus.

No payloads, source paths, credentials, actor identity, or artifact bytes are stored.
No external owner effect can be replayed from this journal.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import sqlite3
from typing import Any

from .errors import AdmissionError

_SHA = re.compile("^[0-9a-f]{64}$")
_ID = re.compile("^[a-zA-Z0-9_.:-]{3,128}$")
_SCHEMA = """
CREATE TABLE IF NOT EXISTS preview_intents (
    key TEXT PRIMARY KEY,
    intent_sha256 TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN ('running','finished','failed','uncertain')),
    output_sha256 TEXT,
    created_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


@dataclass(frozen=True)
class JournalEntry:
    key: str
    intent_sha256: str
    state: str
    output_sha256: str | None
    newly_created: bool = False


class LocalPreviewJournal:
    def __init__(self, path: Path):
        self.path = Path(path)
        if self.path.exists() and self.path.is_symlink():
            raise AdmissionError("JOURNAL_UNSAFE", "Symlink journal is forbidden")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(self.path), timeout=3, isolation_level=None)
        self._db.execute("PRAGMA busy_timeout=3000")
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute("PRAGMA synchronous=FULL")
        self._db.executescript(_SCHEMA)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self) -> None:
        self._db.close()

    def begin(self, key: str, intent_sha256: str) -> JournalEntry:
        if not _ID.fullmatch(key) or not _SHA.fullmatch(intent_sha256):
            raise AdmissionError("JOURNAL_INVALID", "Invalid idempotency key or intent hash")
        self._db.execute("BEGIN IMMEDIATE")
        try:
            row = self._db.execute("SELECT intent_sha256,state,output_sha256 FROM preview_intents WHERE key=?", (key,)).fetchone()
            if row:
                if row[0] != intent_sha256:
                    raise AdmissionError("REPLAY_CONFLICT", "Same key points to different input or configuration")
                value = JournalEntry(key, row[0], row[1], row[2], False)
            else:
                self._db.execute("INSERT INTO preview_intents(key,intent_sha256,state) VALUES(?,?,'running')",
                                 (key, intent_sha256))
                value = JournalEntry(key, intent_sha256, "running", None, True)
            self._db.execute("COMMIT")
            return value
        except Exception:
            self._db.execute("ROLLBACK")
            raise

    def terminal(self, key: str, intent_sha256: str, *, state: str, output_sha256: str | None = None) -> JournalEntry:
        if state not in ("finished", "failed", "uncertain"):
            raise AdmissionError("JOURNAL_INVALID", "Invalid preview terminal state")
        if output_sha256 is not None and not _SHA.fullmatch(output_sha256):
            raise AdmissionError("JOURNAL_INVALID", "Invalid output digest")
        self._db.execute("BEGIN IMMEDIATE")
        try:
            row = self._db.execute("SELECT intent_sha256,state,output_sha256 FROM preview_intents WHERE key=?", (key,)).fetchone()
            if not row or row[0] != intent_sha256:
                raise AdmissionError("JOURNAL_INVALID", "Intent is missing or differs")
            if row[1] != "running":
                if row[1] == state and row[2] == output_sha256:
                    self._db.execute("COMMIT")
                    return JournalEntry(key, intent_sha256, state, output_sha256)
                raise AdmissionError("JOURNAL_RECONCILE", "Terminal entry cannot be rewritten")
            self._db.execute("UPDATE preview_intents SET state=?,output_sha256=?,updated_utc=CURRENT_TIMESTAMP WHERE key=?",
                             (state, output_sha256, key))
            self._db.execute("COMMIT")
            return JournalEntry(key, intent_sha256, state, output_sha256)
        except Exception:
            self._db.execute("ROLLBACK")
            raise

    def inspect(self, key: str) -> JournalEntry | None:
        row = self._db.execute("SELECT intent_sha256,state,output_sha256 FROM preview_intents WHERE key=?", (key,)).fetchone()
        return JournalEntry(key, row[0], row[1], row[2]) if row else None
