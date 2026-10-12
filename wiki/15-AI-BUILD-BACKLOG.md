# AI-build backlog — small, verifiable work packages

**Coding agents:** execute these work packages **sequentially**. Each requires a test and a non-implementation/status report. If an upstream contract is missing or ambiguous, record `[BLOCKED]` and avoid filling it in with invented structures.

## Task D-000 — Freeze baseline

**Read:** `AGENTS.md`, `01-SOURCE-BASELINE.md`, upstream IK/Kristal files.  
**Build:** version/digest inventory and a baseline-check command (offline).  
**Pass:** exact baseline accepted; changed lock rejected; v7 draft pin discrepancy reported, not silently normalized.  
**Forbidden:** modify canonical IK or Kristal schema to satisfy DaaT.

## Task D-001 — Mapping profile manifest validator

**Read:** `04-CONTRACTS-AND-VERSIONS.md`, `06-MAPPING-PROFILES.md`.  
**Build:** reviewed JSON Schema and validator for DaaT-owned `mapping-profile` proposal after ADR.  
**Pass:** rejects missing source/target contract pins, unsupported operations, bad semver and prohibited loss rules.  
**Forbidden:** unpinned JSON transform snippets running arbitrary code.

## Task D-002 — Deterministic mapper

**Build:** `copy`, `rename`, `select`, `construct_object`, `map_enum`, `convert_unit`, `assert`, explicit optional omission.  
**Pass:** identity fixture byte/semantic equivalence where applicable; missing/null distinction tests; rounding and overflow tests; same input+pins means same output.  
**Forbidden:** runtime LLM decisions, network calls from transform rules.

## Task D-003 — Alignment report engine

**Read:** `07-ALIGNMENT-METRICS.md`.  
**Build:** per-rule transformation inventory, coverage, burden, loss and unsupported/ambiguous counts; JSON and human-readable report.  
**Pass:** three fixture classes produce expected values; scope cannot be silently changed; repeated run is stable.  
**Forbidden:** public quality rankings or score inflated by counting only the mapping directory.

## Task D-004 — IK v6 reference compatibility

**Read:** `Interaction-Kernel/adapters/daat/build_mapping.py`, upstream `kristal.build.request/2.0.0` and `artifact.ready/2.0.0`.  
**Build:** bridge from admitted IK interaction + verified source-owned ExportManifest → Kristal-native client port; preserve existing v6 fields.  
**Pass:** owner schema validation; wrong target, mapping ID, v6 pin all rejected; v7-only payload blocked.  
**Forbidden:** inventing a new generic IK profile and labeling it the existing one.

## Task D-005 — Authorization facade

**Read:** `05-ADMISSION-AND-SECURITY.md`; IK security authority docs.  
**Build:** interface using configured trusted auth provider and receiver-local authorization (initially dependency-injected test double).  
**Pass:** wrong issuer/audience, expired identity, cross-tenant and missing capability rejected; zero transform never bypasses auth.  
**Forbidden:** hardcoded production secrets or accepting the sender's claim as proof.

## Task D-006 — Artifact ref and receipt validation

**Build:** owner-schema validation of `ArtifactRef`, acceptance/final receipts and ready events; preserve `owner`, integrity and correlation.  
**Pass:** tampered digest rejects; `reference` stage not invented; `ArtifactRef.owner` stays source/publisher owner.  
**Forbidden:** storing raw artifacts in a DaaT journal or emitting unverified success.

## Task D-007 — Reliable journal and retry (conditional)

**Requires:** agreed durable deployment mode, idempotency policy and storage decision.  
**Build:** minimal process record, duplicate suppression, safe recovery and retry classification.  
**Pass:** same key/digest resumes; same key/different digest blocked; timeout-after-side-effect reconciles without duplicate native invocation.  
**Forbidden:** claiming exactly-once effects absent owner cooperation.

## Task D-008 — External partner adapter starter

**Build:** non-Kristal foreign app sample (`inventory.read`) without using fake IK wire names. Generate schema/fixture/mapping/testing template and integration guide.  
**Pass:** one reviewer can adapt the fixture to a second source model with zero core runtime code changes.  
**Blocked until:** IK authorizes generic external capability Profile before claiming real IK exchange.

## Task D-009 — TCK and CI

**Build:** scripts for schema validation, unit/security/integration tracks; fixtures offline; signed/locked contract dependencies if approved.  
**Pass:** all listed gates in `09-CONFORMANCE-AND-TESTS.md`; repeated builds match; CI prevents accidental DaaT runtime→Orgo/Kristal source code duplication.  
**Forbidden:** green tests based solely on mocks but labeled production integration.

## Task D-010 — Release evidence bundle

**Build:** changelog, verified `manifest.json`, conformance scope report, deployment limitations, generated traceability and operator notes.  
**Pass:** every supported claim links to a test; known gaps are explicit; rollback runbook and release pin matrix available.  
**Forbidden:** inventing certification badges, official approval, or deployed endpoint claims.

## Agent output for each task

```text
Task ID:
Snapshot source baseline:
Files changed:
Implemented behavior:
Commands executed + actual results:
Positive/negative fixtures:
Owner contract(s) reused:
Unresolved decisions / blockers:
New security/privacy risks:
Claimed readiness level:
```

## End-to-end pilot acceptance (strict)

1. An external system's **normal** native export enters through an authorized path.
2. Correct IK Profile, owner, tenant, version and integrity are verified.
3. Mapping is zero-transform **or** every conversion is declared and tested.
4. Owner-native receiver receives a valid compatible contract.
5. A real response is validated and its ownership preserved.
6. IK Receipts/Events or receiver outcomes correlate correctly, including a retry case.
7. Alignment report is reproducible and discloses unsupported/lossy semantics.
8. No secret, raw student data or unauthorized artifact is published.

Passing only steps 1–3 means *mapper prototype*, not an interoperable deployed system.
