# 33 — Implementation-ready roadmap, decisions and acceptance gates

**Status:** `TARGET_DESIGN` for future development. **No code changes are contained in this documentation pack.**  
**Execution posture:** preserve existing DaaT v0.3.0 functionality; deliver narrow, testable steps; never present external connectors or v11 support as existing.  
**Owner approval:** this roadmap is a proposed order of work, not authorization to change another repository's canonical schema.

## 1. Decisions fixed for the implementation design

1. DaaT remains the **single onboarding experience and mapping/admission boundary** for foreign data, not a shared data warehouse, crawler, scheduler, publisher or semantic authority.
2. Use **Kintsugi Mimic/Annex/Reference**: reusable, isolated open-source workers where justified, with pinned versions, rights and credits; the native ecosystem's existing owners remain sovereign.
3. **No new canonical provenance schema.** Reuse existing IK/Kristal references, v11 identity/crosswalk boundaries and Framework profiles; RO-Crate is an optional future export.
4. Maintain independent classifications: access lane, content source archetype, candidate Arketype structures.
5. **Start with safe local PDF and pinned Git snapshots.** Bibliographic metadata follows with provider-specific legal limits; Acomba follows via private read-only sandbox; bulk/CDC only after replay is qualified.
6. Human/domain review plus owner-controlled Kit authoring before canonical promotions. No AI-only inference becomes accepted state.

## 2. Sequenced work packages

| ID | Implementation deliverable | Depends on | Acceptance/stop gate |
|---|---|---|---|
| **W0** | Freeze actual owner contracts, permission and release baseline; verify `Daat` v0.3.0 tests and license policy | IK + Framework/Kit + source owners | Exact version/hash inventory, status matrix, conflicts flagged; no guessing of v11 compatibility |
| **W1** | Static source taxonomy/catalogue, lane selection prototype and adapter manifest validator (offline) | W0 | 36 families parse; malformed/unlicensed/unsupported declaration rejected; **no runtime source reads** |
| **W2** | Pure extraction result/evidence-reference interface + deterministic mapping and fixture runner | W0–W1 | Source-location anchors, loss report, pinned Golden+malicious fixtures, no network from DSL |
| **W3** | PDF connector prototype using bounded local files and optional Docling worker | W2 + legal/security review | Sandbox, source hashes/page anchors, no secret leaking, no AI canonical writes |
| **W4** | Git read-only pinned-commit connector prototype | W2 + repo grant policy | Commit+blob references, no code execution or untrusted submodule traversal, negative tests |
| **W5** | Source-owner custody and IK/Konfid integration **only through approved contracts** | Owner ADRs and trusted host | Bilateral positive/negative tests; real source authorization; deny-by-default; correct terminal receipts |
| **W6** | Kristalizer/diK/Arketype review + Kit handoff at **exact adopted owner version** | W5 and Framework/Kit acceptance | Candidate remains noncanonical until owner review; valid local build only, not publication |
| **W7** | Scholarly metadata pilot (authorized provider) | W3–W6 semantics | DOI/author collisions, ToS constraints, versioned deltas, no unauthorized full-text mirror |
| **W8** | Acomba read-only private sandbox pilot | W3–W6 + actual SDK/export grants | Ledger semantic distinctions, cross-tenant security, snapshot consistency, no source write |
| **W9** | Operational reliability: durable cursor/checkpoint, idempotency/outbox, corrections, audit, revocation | Owner-approved live runtime | Crash/restart, duplicate/conflict, uncertain-effect reconciliation; privacy/legal review |
| **W10** | Optional bulk/stream/enterprise sidecars and externally facing SDK/service | W9 plus measured demand | Scalability and independent security qualification; no second event bus |

**Concurrency:** W3 and W4 can progress in parallel after W2. W5/6 are **blocked on owner-approved ingress/authoring contracts**; do not manufacture a fake successful integration to get past them. W7/8 sandbox experiments may produce noncanonical local fixtures before W6, but **may not be declared integrated**.

## 3. Explicit owner decision register

| Decision | Owner | Present status | Required evidence |
|---|---|---|---|
| Generic external IK ingress and its authenticated host | Interaction Kernel + kOA security/receivers | **BLOCKED / not adopted** | ADR, schema/profile ID, sender privileges, producer/consumer TCK |
| Médiathèque source-reference disclosure to DaaT | Médiathèque + source owner | **BLOCKED / not adopted** | scoped ACL/receipt/locator contract and bilateral tests |
| v11 Framework/Kit/diK integration target and compatible exact revisions | Framework, Kit, diK/Kristalizer | **BLOCKED until pinned owner proof** | schemas, fixtures, approval and crosswalk review |
| DaaT code/docs license + copied upstream schema redistribution | DaaT owner and upstream owners | **PENDING** in `LICENSE-POLICY.md` | legal review, SPDX IDs/notices, authorized owner contract distribution |
| Sidecar selections / model assets | DaaT product+security+legal | **PROPOSED only** | exact tag/commit/license/SBOM, threat and replay tests |
| Source-specific rights (PhilPapers, Acomba, etc.) | Source rights holder + ingesting tenant | **MUST VERIFY per source** | terms, credentials, use grants, privacy and retention |
| Durable service / event delivery runtime | IK, Orgo and platform owners | **NOT SELECTED** | ADR excluding duplicate bus/scheduler, recovery and audit plan |
| Future RO-Crate and PROV-O exporters | Framework/projection owners | **OPTIONAL** | exact version and independent conformance, not DaaT core schema |

This register **extends**, not overrides, [14 — Open decisions](14-OPEN-DECISIONS.md). Any owner conflict stops only the affected feature.

## 4. Initial coding backlog: first ten concrete pull requests

1. Baseline verification: reproducible test run, exact owner profile inventory and doc links.
2. `source-family` static catalogue validation + tests (no network, no source payload).
3. Adapter metadata declaration model (non-wire) + strict validator with reject fixtures.
4. Extracted-evidence reference port with page/commit/record anchors and source digest handling.
5. Mapping fixture harness over approved owner schema locks; malicious inputs and semantic loss tests.
6. Local PDF import *adapter in a sandbox* with bounded PDF fixture and versioned extraction.
7. Pinned Git snapshot reader with safe path rules and deterministic repository fixture.
8. Candidate classification/review surface (off-line suggestions only) with explicit uncertainty provenance.
9. Owner integration ADR proposals + consumer fixture pack, before any public transport.
10. Source-specific legal, security and SBOM register with version-pinned optional worker selection.

For each PR comply with `AGENTS.md`: `[UPSTREAM-FACT]`, `[OWNER-DECISION]`, `[PROPOSAL]`, `[BLOCKED]`, `[TESTED]`; command output, negative fixture, rollback/recovery and actual status must be attached. A PR must **not** claim completed TCK merely because synthetic code passes.

## 5. Documentation definition of done (this package)

- /docs explains universal source onramp, eight access lanes, 36-family research matrix, Kintsugi/Kompendio, native standards, pilot journeys, security, conformance, owner handoffs, blocks and coding order.
- C0 repository has a read-only final-system target map, cross-links to FC-01/02/03/04/05/23 and keeps owner precedence intact.
- Existing v0.3 release facts are not overwritten; proposed milestones are clearly marked.
- Every new Markdown page is linked from a local index; a subsequent coder can start at W0/PR1 without architectural guesswork.
- No new API contract, application code, license decision, production claim or upstream release authorization is silently introduced.

**Next action after pack review:** start W0 and W1 in the **Daat** code repository; keep the C0 repository as documentation/coordination only.
