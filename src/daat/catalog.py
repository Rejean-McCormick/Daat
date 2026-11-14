"""Static, metadata-only inventory of source families and reviewed access lanes.

A catalogue entry declares *possibilities*, never approved access, licensing,
production support or evidence that a remote provider can be harvested.
"""
from __future__ import annotations
import csv
import io
from dataclasses import dataclass
from importlib.resources import files
from typing import Any

from .errors import DaatError

LANES = {
    "L1": "local_artifacts", "L2": "read_api", "L3": "harvest_export",
    "L4": "bulk_snapshot", "L5": "versioned_tree", "L6": "enterprise_database",
    "L7": "event_stream", "L8": "federated_reference",
}
_REQUIRED = {"id", "famille", "exemples", "formats_et_protocoles", "meilleur_pont",
             "mode_synchronisation", "arketype_candidats", "risques_ou_obligations", "priorite"}

@dataclass(frozen=True)
class SourceFamily:
    id: str
    label: str
    examples: str
    protocols: str
    suggested_bridge: str
    synchronization: str
    candidate_arketypes: tuple[str, ...]
    risks: str
    priority: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "examples": self.examples,
                "protocols": self.protocols, "suggested_bridge": self.suggested_bridge,
                "synchronization": self.synchronization,
                "candidate_arketypes": list(self.candidate_arketypes),
                "risks": self.risks, "priority": self.priority,
                "implementation_status": "research_only_not_a_connector"}


def read_catalogue(text: str) -> tuple[SourceFamily, ...]:
    rows = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    if not rows.fieldnames or set(rows.fieldnames) != _REQUIRED:
        raise DaatError("CATALOG_INVALID", "Unexpected source catalogue columns")
    catalog: list[SourceFamily] = []
    seen: set[str] = set()
    for r in rows:
        if not r or any(not isinstance(v, str) or not v.strip() for v in r.values()):
            raise DaatError("CATALOG_INVALID", "Missing catalogue data")
        identifier = r["id"]
        if len(identifier) != 2 or not identifier.isdigit() or identifier in seen:
            raise DaatError("CATALOG_INVALID", "Duplicate or malformed source ID")
        seen.add(identifier)
        archetypes = tuple(s.strip() for s in r["arketype_candidats"].split(","))
        if not archetypes or any(not s.startswith("ARK-") or len(s) != 6 or not s[-2:].isdigit() for s in archetypes):
            raise DaatError("CATALOG_INVALID", "Malformed advisory Arketype references")
        catalog.append(SourceFamily(identifier, r["famille"], r["exemples"],
                                    r["formats_et_protocoles"], r["meilleur_pont"],
                                    r["mode_synchronisation"], archetypes,
                                    r["risques_ou_obligations"], r["priorite"]))
    if len(catalog) != 36:
        raise DaatError("CATALOG_INVALID", "Expected the documented 36 source families")
    return tuple(catalog)


def source_families() -> tuple[SourceFamily, ...]:
    resource = files("daat").joinpath("resources", "data", "source-family-landscape-36.csv")
    return read_catalogue(resource.read_text(encoding="utf-8-sig"))


def source_family(identifier: str) -> SourceFamily:
    for item in source_families():
        if item.id == identifier:
            return item
    raise DaatError("CATALOG_UNKNOWN", "Unknown source family")
