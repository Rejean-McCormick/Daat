"""Offline onramp registration and trust-boundary regression fixtures."""
from __future__ import annotations
import json
import pytest
from pathlib import Path

from daat.catalog import source_families, read_catalogue, source_family, LANES
from daat.errors import DaatError, AdmissionError
from daat.registry import AdapterRegistry, builtin_registry, validate_adapter_manifest
from daat.source import RightsDeclaration, ReadLimits, SourceSelection, confined_path


def rights() -> RightsDeclaration:
    return RightsDeclaration("test-tenant", "test-export", "test-owned", "test-user", True)


def test_all_36_families_are_research_metadata_only():
    families = source_families()
    assert len(families) == 36
    assert len({f.id for f in families}) == 36
    assert all(f.to_dict()["implementation_status"] == "research_only_not_a_connector" for f in families)
    assert len(LANES) == 8
    assert source_family("11").candidate_arketypes


def test_catalog_denies_incorrect_or_duplicated_ids():
    with pytest.raises(DaatError):
        source_family("37")
    valid = "id,famille,exemples,formats_et_protocoles,meilleur_pont,mode_synchronisation,arketype_candidats,risques_ou_obligations,priorite\n"
    with pytest.raises(DaatError):
        read_catalogue(valid)


def test_builtin_reader_registry_is_explicit_and_bounded():
    reg = builtin_registry()
    items = reg.list()
    assert len(items) == 6
    assert all(item["read_only"] and item["implementation"] == "built_in" for item in items)
    assert all(item["approved_owner_profile"] is None for item in items)
    assert reg.resolve(SourceSelection(Path("."), "example.pdf", "pdf", "08", rights()))[0]["id"] == "local.pdf"
    with pytest.raises(AdmissionError):
        reg.resolve(SourceSelection(Path("."), "unknown.xyz", "acomba", "11", rights()))


def test_manifest_must_not_admit_unapproved_runtime_or_write():
    item = next(m for m in builtin_registry().list() if m["id"] == "local.git")
    item.pop("implementation_status")
    assert validate_adapter_manifest(item)["lane"] == "L5"
    item["read_only"] = False
    with pytest.raises(AdmissionError):
        validate_adapter_manifest(item)
    item["read_only"] = True
    item["approved_owner_profile"] = "kristal.build.request/2.0.0"
    with pytest.raises(AdmissionError):
        validate_adapter_manifest(item)


def test_adapters_do_not_load_scripts_from_manifest():
    reg = AdapterRegistry()
    item = next(m for m in builtin_registry().list() if m["id"] == "local.git")
    item.pop("implementation_status")
    item["implementation"] = "trusted_host_worker"
    with pytest.raises(AdmissionError):
        reg.register(item, lambda _: None)


def test_root_and_rights_reject_invalid_user_input(tmp_path):
    with pytest.raises(AdmissionError):
        RightsDeclaration("test-tenant", "research", "terms", "person", False)
    with pytest.raises(AdmissionError):
        RightsDeclaration("test-tenant", "research", "terms", "person", "true")
    with pytest.raises(AdmissionError):
        confined_path(tmp_path, "../secret.txt")
    with pytest.raises(AdmissionError):
        confined_path(tmp_path, str(tmp_path / "file.txt"))
    with pytest.raises(AdmissionError):
        ReadLimits(max_source_bytes=-1)
    with pytest.raises(AdmissionError):
        SourceSelection(tmp_path, "a", "pdf", "not_a_family", rights())
