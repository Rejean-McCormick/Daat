from __future__ import annotations
from io import BytesIO
import zipfile
import pytest
from daat.source import SourceSelection, RightsDeclaration, ReadLimits
from daat.pipeline import prepare_local
from daat.errors import AdmissionError


def snapshot(tmp_path):
    return SourceSelection(tmp_path, "docs.zip", "archive", "09",
                           RightsDeclaration("tenant-x", "research", "owner-granted", "actor-x", True))


def test_zip_has_bounded_nested_record_anchors(tmp_path):
    with zipfile.ZipFile(tmp_path / "docs.zip", "w") as z:
        z.writestr("set/data.csv", "name,value\na,1\nb,2\n")
        z.writestr("set/readme.md", "Read this as source text, not instructions")
    batch = prepare_local(snapshot(tmp_path))
    assert len(batch["records"]) == 3
    assert "docs.zip!set/data.csv" in batch["records"][0]["anchor"]["location"]
    assert batch["owner_handoff"].startswith("blocked")


def test_zip_path_traversal_or_nested_archive_forbidden(tmp_path):
    with zipfile.ZipFile(tmp_path / "docs.zip", "w") as z:
        z.writestr("../outside.csv", "a\n1")
    with pytest.raises(AdmissionError):
        prepare_local(snapshot(tmp_path))
    with zipfile.ZipFile(tmp_path / "docs.zip", "w") as z:
        z.writestr("bundle.zip", "nested")
    with pytest.raises(AdmissionError):
        prepare_local(snapshot(tmp_path))


def test_zip_ratio_limit_rejects_compression_bomb(tmp_path):
    with zipfile.ZipFile(tmp_path / "docs.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("data.txt", "A" * 500_000)
    with pytest.raises(AdmissionError):
        prepare_local(snapshot(tmp_path))


def test_pdf_magic_rejects_non_pdf_without_dependency(tmp_path):
    (tmp_path / "fake.pdf").write_bytes(b"not a pdf")
    source = SourceSelection(tmp_path, "fake.pdf", "pdf", "08",
                             RightsDeclaration("tenant-x", "test", "owned", "actor-x", True))
    with pytest.raises(AdmissionError) as failure:
        prepare_local(source)
    assert failure.value.code == "SOURCE_PDF_INVALID"


def test_pdf_positive_optional_parser(tmp_path):
    pypdf = pytest.importorskip("pypdf")
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=300, height=300)
    with (tmp_path / "paper.pdf").open("wb") as output:
        writer.write(output)
    source = SourceSelection(tmp_path, "paper.pdf", "pdf", "08",
                             RightsDeclaration("tenant-x", "test", "owned", "actor-x", True))
    batch = prepare_local(source)
    assert len(batch["records"]) == 1
    assert batch["records"][0]["anchor"]["kind"] == "pdf_page"
