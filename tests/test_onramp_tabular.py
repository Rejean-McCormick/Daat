from __future__ import annotations
import json
from pathlib import Path
import pytest
from daat.source import SourceSelection, RightsDeclaration, ReadLimits
from daat.errors import AdmissionError
from daat.pipeline import prepare_local, concise_report
from daat.verification import verify_preparation
from daat.cli import main


def make_source(tmp_path, name="data.jsonl", *, kind="dataset", family="07", record_type=None):
    return SourceSelection(tmp_path, name, kind, family,
                           RightsDeclaration("tenant-a", "research", "owned-data", "actor-a", True),
                           record_type=record_type)


def test_jsonl_extracts_anchored_records_without_canonicalizing(tmp_path):
    (tmp_path / "data.jsonl").write_text('{"id":"outside:11","measurement":3}\n{"id":"outside:12","measurement":4}\n', encoding="utf-8")
    preview = prepare_local(make_source(tmp_path))
    assert len(preview["records"]) == 2
    assert preview["records"][0]["anchor"]["location"].endswith("line:1")
    assert all(c["semantic_identity"] is None for c in preview["candidates"])
    assert preview["authority"] == "noncanonical_unreviewed"
    assert verify_preparation(preview)["valid"]
    assert concise_report(preview)["record_count"] == 2


def test_reference_only_retains_hash_without_content(tmp_path):
    (tmp_path / "data.jsonl").write_text('{"id":"a"}\n', encoding="utf-8")
    s = make_source(tmp_path)
    s = SourceSelection(s.root, s.relative_path, s.kind, s.family_id, s.rights, mode="reference")
    prepared = prepare_local(s)
    assert prepared["records"] == []
    assert prepared["candidates"] == [] if "candidates" in prepared else True
    assert prepared["source"]["mode"] == "reference"


def test_integrity_hash_detects_changed_content(tmp_path):
    (tmp_path / "data.jsonl").write_text('{"id":"a"}\n', encoding="utf-8")
    output = prepare_local(make_source(tmp_path))
    output["records"][0]["data"]["id"] = "tampered"
    with pytest.raises(AdmissionError):
        verify_preparation(output)


def test_unknown_json_duplicate_key_or_invalid_csv_rejected(tmp_path):
    (tmp_path / "data.jsonl").write_text('{"id":"a","id":"b"}\n', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(make_source(tmp_path))
    (tmp_path / "data.csv").write_text('id,id\na,b\n', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(make_source(tmp_path, "data.csv"))


def test_malformed_bounded_json_rejected(tmp_path):
    (tmp_path / "data.jsonl").write_text('{"id":1e999}\n', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(make_source(tmp_path))
    (tmp_path / "data.jsonl").write_text('"string"\n', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(make_source(tmp_path))


def test_source_symlink_refused_if_os_allows_it(tmp_path):
    source = tmp_path / "real.jsonl"
    source.write_text('{"id":"a"}\n', encoding="utf-8")
    link = tmp_path / "link.jsonl"
    try:
        link.symlink_to(source)
    except (OSError, NotImplementedError):
        pytest.skip("Host cannot create symlinks")
    with pytest.raises(AdmissionError):
        prepare_local(make_source(tmp_path, "link.jsonl"))


def test_cli_requires_rights_but_does_not_print_source_payload(tmp_path, capsys):
    (tmp_path / "data.jsonl").write_text('{"text":"private_marker_abc","id":"x"}\n', encoding="utf-8")
    args = ["prepare-local", "--root", str(tmp_path), "--source", "data.jsonl", "--kind", "dataset",
            "--family", "07", "--tenant", "tenant-a", "--actor", "actor-a", "--purpose", "test",
            "--license", "owned"]
    assert main(args) == 2
    assert main(args + ["--rights-acknowledged"]) == 0
    printed = capsys.readouterr()
    assert "private_marker_abc" not in printed.out + printed.err
    assert "record_count" in printed.out
