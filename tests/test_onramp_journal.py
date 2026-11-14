from __future__ import annotations
import json
from pathlib import Path
import pytest

from daat.journal import LocalPreviewJournal
from daat.errors import AdmissionError
from daat.output import write_private_json
from daat.util import json_digest
from daat.cli import main


def test_preview_journal_replay_and_conflict(tmp_path):
    path = tmp_path / "intent.db"
    with LocalPreviewJournal(path) as journal:
        created = journal.begin("intent-one", "a"*64)
        assert created.newly_created
        assert not journal.begin("intent-one", "a"*64).newly_created
        with pytest.raises(AdmissionError):
            journal.begin("intent-one", "b"*64)
        result = journal.terminal("intent-one", "a"*64, state="finished", output_sha256="c"*64)
        assert result.state == "finished"
        assert journal.inspect("intent-one").output_sha256 == "c"*64
        with pytest.raises(AdmissionError):
            journal.terminal("intent-one", "a"*64, state="failed")
    with LocalPreviewJournal(path) as journal:
        assert journal.inspect("intent-one").state == "finished"


def test_private_output_rejects_implicit_replace(tmp_path):
    path = tmp_path / "result.json"
    write_private_json(path, {"source":"secret"})
    assert json.loads(path.read_text(encoding="utf-8")) == {"source":"secret"}
    with pytest.raises(AdmissionError):
        write_private_json(path, {"source":"changed"})
    write_private_json(path, {"source":"changed"}, replace=True)
    assert json.loads(path.read_text(encoding="utf-8"))["source"] == "changed"


def test_journaled_cli_does_not_replay_finished_intent(tmp_path):
    (tmp_path / "records.jsonl").write_text('{"id":"one"}\n', encoding="utf-8")
    path = tmp_path / "preview.json"
    journal = tmp_path / "journal.sqlite"
    cmd = ["prepare-local", "--root", str(tmp_path), "--source", "records.jsonl", "--kind", "dataset",
           "--family", "07", "--tenant", "tenant-x", "--actor", "actor-x",
           "--purpose", "research", "--license", "owner-grant", "--rights-acknowledged",
           "--out", str(path), "--journal", str(journal), "--intent-key", "test-snapshot-1"]
    assert main(cmd) == 0
    assert main(cmd + ["--replace"]) == 2
    assert main(["verify-local-preview", str(path)]) == 0
    assert main(["inspect-journal", str(journal), "test-snapshot-1"]) == 0


def test_journal_does_not_store_source_data(tmp_path):
    with LocalPreviewJournal(tmp_path / "j.db") as journal:
        journal.begin("intent-a", "a"*64)
    binary = (tmp_path / "j.db").read_bytes()
    assert b"user-private-payload" not in binary
