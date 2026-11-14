# 34 — Source and status traceability for the DaaT onramp specification

**This document is a navigation map, not an owner-contract duplication.** Source archive: user-provided `SmartDump_20261113_155059.zip`, inspected 2026-11-13; separate GitHub branch-head references are recorded in the update pack manifest. Snapshot files demonstrate their contained text, **not** a production deployment or automatically the current/approved owner release.

## DaaT owner repository

| Source | Governs |
|---|---|
| `AGENTS.md` | Agent stop conditions, trust boundaries and PR evidence |
| `docs/01-SOURCE-BASELINE.md` | Historical source assertions and known version conflicts |
| `docs/02-VISION-AND-INVARIANTS.md` | Product intent and no-second-authority rule |
| `docs/03-ARCHITECTURE.md` | DaaT admitted mapping and owner roles |
| `docs/04-CONTRACTS-AND-VERSIONS.md` | Exact IK/Kristal compatibility scope |
| `docs/06-MAPPING-PROFILES.md` | Declarative deterministic mapping vs prohibited inference |
| `docs/09-CONFORMANCE-AND-TESTS.md` | Existing test categories and C4 not passed |
| `docs/14-OPEN-DECISIONS.md` | Unresolved approvals |
| `docs/19-IMPLEMENTATION-STATUS.md` | v0.3.0 observed implementation, not production |
| `docs/20-SECURITY-BOUNDARY.md` and `21-KONFID-CONTRACT-ALIGNMENT.md` | Actual security PEP and external dependency gaps |
| `docs/23-THREAT-AND-TRUST-MATRIX.md` | Security attacks and denial cases |
| `docs/25-SOURCE-CUSTODY-BOUNDARY.md` | Acquisition/custody/authoring separation |
| `LICENSE-POLICY.md` | DaaT and vendored owner contract licensing undecided |

## Owner-system anchors from the snapshot

| Owner | Source path / note | No implied decision |
|---|---|---|
| Interaction Kernel | `interaction_kernel/docs/adrs/ADR-IK-07-daat-kristal-v7-boundary.md`; `interaction_kernel/adapters/daat/README.md`; adopted `contracts/profiles/kristal/kristal.build.request/2.0.0/` | Existing build profile is not generic external ingress |
| Kristal Framework v5 | `spec/v5/05-profiles/profile-provenance-nanopub-provo.md` | Optional Draft profile; not verified v11 exporter |
| Kristal Framework v9 | `spec/v9/Logical-Artifacts.md`; `docs/08_AUTHORITY_PROVENANCE_AND_TRUST.md` | Do not flatten artifact polymorphism or provenance authority |
| Kristal Framework v11 | `spec/v11/diK-Interoperability.md`; `schemas/v11/` | Proposed v11 graph/crosswalk semantics are owner controlled |
| Arketype | `arketype/docs/14_FRAMEWORK_V11_ET_DIK.md`; `arketype/archetypes/` | 19 design archetypes, not KQ/P identifiers |
| Authoring Kit / Kristalizer | Owner-supplied source snapshots in SmartDump | Exact compatible target to be pinned, not invented |
| kOA central target | `docs/target/functional-chains/` (read from current central public repo; absent from bundled central snapshot) | Target design, not operational qualification |
| Kintsugi reference | User-provided ethiKos, keenKonnect, KonnectED and Konnaxion documents | Mimic/Annex/Kompendio patterns, not a DaaT owner contract |

## Research status discipline

- `SOURCE-BACKED`: observed text/implementation in provided source snapshot at its actual version.
- `USER_DECIDED`: product direction explicitly requested in this conversation (universal DaaT onramp; Kristal remains canonical; Kintsugi reuse/credits).
- `TARGET_DESIGN` or `PROPOSED`: authored architecture and acceptance guidance to be reviewed before implementation.
- `BLOCKED`: owner contract or operational/legal qualification has not been supplied.
- `TESTED`: only for a test actually executed on a named source revision/environment, not inferred from a document.

**External sources are references, not licenses:** [W3C PROV-O](https://www.w3.org/TR/prov-o/), [RO-Crate](https://www.researchobject.org/ro-crate/), [SPDX](https://spdx.dev/), [CycloneDX](https://cyclonedx.org/), plus exact upstream software repositories to be pinned during implementation. The source family matrix is an exploratory research catalogue, not approved source redistribution rights.
