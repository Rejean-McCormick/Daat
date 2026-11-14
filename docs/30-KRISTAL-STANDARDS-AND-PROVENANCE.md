# 30 — Native Kristal interoperability and provenance: use what already exists

**Status:** `SOURCE-BACKED` for cited historical contracts and `TARGET_DESIGN` for future DaaT usage. No format migration is authorized.  
**Critical rule:** **Kristal is canonical. PROV-O, RDF/JSON-LD, nanopublications and RO-Crate are *optional external representations*, not replacement state or a second provenance ledger.**

## 1. Owner formats already solve the essential problem

The inspected Framework history includes:

| Existing capability | Owner source (snapshot-relative) | Interpretation |
|---|---|---|
| v5 optional provenance/nanopublications | `Kristal-Framework/spec/v5/05-profiles/profile-provenance-nanopub-provo.md` | Draft profile `kristal.v5:provenance-nanopub-provo` v2.0: Head, Assertion, Provenance, PubInfo and PROV-O relations |
| v5 JSON-LD/RDF projection | `Kristal-Framework/spec/v5/05-profiles/profile-jsonld-export.md`, `profile-rdf-wdqs-export.md` | Standards-facing export profiles, not alternate canonical identities |
| v5 state/evidence/exchange/runtime pack | `Kristal-Framework/spec/v5/02-schemas/` | Assertions, provenance, source/evidence references, manifests, build inputs and checksum material |
| Three distinct provenance layers | `Kristal-Framework/docs/08_AUTHORITY_PROVENANCE_AND_TRUST.md` | Epistemic, build and publication provenance must not be collapsed |
| v9 polymorphic logical artifacts | `Kristal-Framework/spec/v9/Logical-Artifacts.md` | Do not impose a universal DaaT `nodes/edges/rows` object on every Kristal |
| v11 semantic/lexical/crosswalk boundaries | `Kristal-Framework/spec/v11/diK-Interoperability.md` and `schemas/v11/` | KQ/KP/KA/KS are owner-issued; external Wikidata Q/P remain separate |
| IK source-owned references and exchange metadata | DaaT's pinned `contracts/owners/ik/{artifact-ref,export-manifest,receipt,envelope}.schema.json` | A reference or receipt never transfers custody, trust or recognition |

**Do not generalize historical v5 profile existence into v11 implementation readiness.** The v5 PROV-O document is explicitly a **Draft optional profile**. Exact v11 adoption, producer support and conformance must be independently checked. The present DaaT v0.3 path is pinned to portable Kristal v6, not a general v11 authoring API.

## 2. Three provenance dimensions

1. **Epistemic:** source assertions and evidentiary relations, confidence/valuation and applicability, disputes, recognition and authority. A source reference is not a truth claim.
2. **Build:** pinned source snapshot, transform profile and version, toolchain/model identity, configuration, deterministic derivations, and checksums. A build proves reproducibility of a transformation, not factual correctness.
3. **Publication:** explicit release approval, signing, distribution destination and runtime activation. A signature is not epistemic validation or authority recognition.

For a content import, preserve all three separately, and record missing components as unknown or blocked rather than manufacturing facts.

## 3. Source identities versus semantic identities

- Persist external DOI, account, Git commit, document URI and Wikidata `Q...`/`P...` in their proper **external namespaces**.
- Do not manufacture canonical KQ/KP from matching words, embeddings, DOI matches or external Q/P values.
- A reviewed crosswalk records relation type, scope, evidence and decision. A `closeMatch` must not become `exactMatch` by convenience.
- diK lexical dictionaries and alignment crosswalks are separate. A translated label cannot establish semantic identity.
- The Framework/Kit decide when a proposed assertion becomes canonical KA with its KS source reference; Arketype designs alone never establish this.

## 4. External export compatibility

| Requested external representation | DaaT policy |
|---|---|
| PROV-O / nanopublications | Prefer existing Framework profile where **supported at exact version**; test with named-graph and provenance fixtures |
| JSON-LD / RDF | Use existing owner export profiles and verify pinned producer/consumer versions |
| RO-Crate | If a partner requires it, propose a **separate optional export projection** from existing approved manifests and refs; validate `ro-crate-metadata.json` and JSON-LD graph with external validators; never change canonical Kristal |
| DOI/BibTeX/CSL-JSON, MARC, JSONL/Parquet, Git or proprietary outputs | Format at the source/adapter edge; do not rewrite the Framework vocabulary |

RO-Crate structural similarity is not proof that a Kristal Runtime Pack is already RO-Crate-conformant. An export must be declared, reproducible and tested for the requested target profile. No such exporter is authorized or required for DaaT v1.

## 5. Contract/compatibility matrix

| Existing/target surface | Current posture | Developer response |
|---|---|---|
| IK `ik/1.1` + `kristal.build.request/2.0.0` | Observed DaaT v0.3 tests with v6 locks | Preserve exact pins and authorized sender semantics |
| Local `daat.mapping-profile/0.2.0-draft` | Offline tool profile, *not* adopted IK wire | Permit only local declared transformations and fixtures |
| Kristal Framework v7–v11 drafts | Owner-evolving, different scopes/revisions | No silent reinterpretation or automatic migrations; owner-approved exact profile + bilateral tests |
| Médiathèque source-ref admission | Not adopted as generic DaaT↔Médiathèque profile | Block until relevant owners adopt disclosure/ingress contracts |
| RO-Crate export | Optional future research | Reference only, no new canonical schema |

## 6. Acceptance checks

- Exact source and target profile digests are verified; rejected when mismatched.
- Every admitted candidate retains source identity and original epistemic qualifiers, along with any declared omissions.
- External Q/P remain external identifiers; collisions and homonyms are reviewed.
- v5 exporter, if used, is tested with fixture, stable graph IDs and its supported serialization/version, never claimed as generic v11 support.
- A local build cannot bypass independent qualification, public release consent or activation controls.

**References:** [04 — Contracts and versions](04-CONTRACTS-AND-VERSIONS.md); [06 — Mapping profiles](06-MAPPING-PROFILES.md); [25 — Custody boundary](25-SOURCE-CUSTODY-BOUNDARY.md); [32 — Conformance](32-TEST-AND-THREAT-PLAN.md). External standards: [W3C PROV-O](https://www.w3.org/TR/prov-o/), [RO-Crate 1.1](https://www.researchobject.org/ro-crate/specification/1.1/).
