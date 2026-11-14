from __future__ import annotations
import pytest
from daat.diagnosis import diagnose_local
from daat.source import RightsDeclaration
from daat.errors import AdmissionError


def rights():
    return RightsDeclaration("tenant-x", "review", "owned", "actor-x", True)


def test_diagnostic_suggests_not_asserts_family(tmp_path):
    (tmp_path / "sample.csv").write_text("id\n1\n", encoding="utf-8")
    result = diagnose_local(tmp_path, "sample.csv", rights())
    assert result["source_kind_hint"] == "dataset"
    assert any(row["family_id"] == "13" for row in result["candidates"])
    assert all(row["verification"] == "heuristic_unreviewed" for row in result["candidates"])


def test_diagnostic_refuses_fake_pdf(tmp_path):
    (tmp_path / "fake.pdf").write_text("not PDF", encoding="utf-8")
    with pytest.raises(AdmissionError):
        diagnose_local(tmp_path, "fake.pdf", rights())
