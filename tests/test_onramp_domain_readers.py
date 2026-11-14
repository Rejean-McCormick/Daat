from __future__ import annotations
import json
import pytest

from daat.source import SourceSelection, RightsDeclaration
from daat.pipeline import prepare_local
from daat.errors import AdmissionError


def selection(tmp_path, name, kind, family, record_type=None):
    return SourceSelection(tmp_path, name, kind, family,
                           RightsDeclaration("tenant-f", "analysis", "local-owner-license", "actor-f", True),
                           record_type=record_type)


def test_bibliography_preserves_doi_and_reports_duplicates(tmp_path):
    rows = [{"title":"Preprint", "DOI":"10.1234/ABC", "author":"A"},
            {"title":"Publication", "doi":"https://doi.org/10.1234/abc", "author":"A"},
            {"title":"Different", "doi":"10.9999/different"}]
    (tmp_path / "meta.json").write_text(json.dumps(rows), encoding="utf-8")
    result = prepare_local(selection(tmp_path, "meta.json", "bibliography", "01"))
    assert len(result["records"]) == 3
    assert result["records"][0]["data"]["doi"] == "10.1234/abc"
    assert any("possible_duplicate_doi" in warning for warning in result["warnings"])
    assert len(result["candidates"]) == 3  # never merge claims on matching DOI


def test_bibliography_ris_and_xml_bounded(tmp_path):
    (tmp_path / "meta.ris").write_text("TY  - JOUR\nTI  - Sample\nDO  - 10.1234/abc\nER  - \n", encoding="utf-8")
    batch = prepare_local(selection(tmp_path, "meta.ris", "bibliography", "01"))
    assert len(batch["records"]) == 1
    (tmp_path / "meta.xml").write_text('<records><record><title>Example</title><identifier>doi:10.1234/foo</identifier></record></records>', encoding="utf-8")
    assert len(prepare_local(selection(tmp_path, "meta.xml", "bibliography", "01"))["records"]) == 1


def test_unsafe_bibliography_xml_entities_denied(tmp_path):
    (tmp_path / "meta.xml").write_text('<!DOCTYPE foo [<!ENTITY a "fake">]><records><record><title>&a;</title></record></records>', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(selection(tmp_path, "meta.xml", "bibliography", "01"))


def test_bibliography_invalid_doi_rejected(tmp_path):
    (tmp_path / "meta.json").write_text('[{"DOI":"not-a-doi"}]', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(selection(tmp_path, "meta.json", "bibliography", "01"))


def test_acomba_requires_declared_entity_type_and_currency(tmp_path):
    (tmp_path / "invoices.csv").write_text("invoice_id,amount,currency,status\nI-01,100.25,CAD,partial\n", encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(selection(tmp_path, "invoices.csv", "acomba", "13"))
    good = prepare_local(selection(tmp_path, "invoices.csv", "acomba", "13", "invoices"))
    assert good["records"][0]["record_type"] == "accounting_export_invoices"
    assert good["records"][0]["data"]["amount"] == "100.25"
    (tmp_path / "no_currency.csv").write_text("amount\n100.25\n", encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(selection(tmp_path, "no_currency.csv", "acomba", "13", "payments"))


def test_acomba_rejects_float_money(tmp_path):
    (tmp_path / "ledger.json").write_text('[{"amount": 100.5, "currency": "CAD"}]', encoding="utf-8")
    with pytest.raises(AdmissionError):
        prepare_local(selection(tmp_path, "ledger.json", "acomba", "13", "payments"))
