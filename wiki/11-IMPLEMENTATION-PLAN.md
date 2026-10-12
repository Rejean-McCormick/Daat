# Incremental construction plan for DaaT

This document defines implementable milestones for an AI agent or engineering team. Each step has an explicit result and exit criteria. It is **not** a claim that the code already exists in this documentation-only repository.

## Milestone 0 — Governance and exact baseline (P0)

**Input:** source snapshots and ADRs. **Output:** pinned contract inventory + compatibility report.

Tasks:

1. Record owner of each canonical schema/profile and exact digest, including IK `ik/1.1`, `kristal.build.request/2.0.0`, portable Kristal v6.
2. Read IK `ADR-IK-07` and Kristal `DaaT-Boundary` before coding.
3. Resolve documented IK v7 draft.3.1 versus Kristal v7 draft.3.2 pin skew with an explicit compatibility decision; do **not** change portable v6 build surface.
4. Decide target package boundary, license, runtime language and private testing topology.
5. Prepare baseline TCK fixtures and negative cases.

**Done when:** immutable artifact manifest exists; source owner approvals or open items recorded; compatibility validator detects tampered locks.

## Milestone 1 — Pure mapping / alignment library (P0)

- Add `MappingProfile` declaration schema (after ADR approval) and a restricted deterministic transform interpreter.
- Implement contract pin verification using owner-provided schemas.
- Implement a zero-semantic-transform validator with identity/provenance preservation checks.
- Implement raw alignment metrics and a structured report. Do not publish a single opaque score.
- Provide 3 fixture classes: identity, simple alias, mandatory-loss rejection.

**Done when:** pinned fixtures have reproducible hashes, no I/O from transform DSL, all negative tests pass and output contracts validate.

## Milestone 2 — IK v6 compatibility path (P0)

- Reuse `interaction_kernel/adapters/daat/build_mapping.py` behavior and existing `MappingProfile` / `KristalNativeClient` protocols.
- Validate actual complete IK envelopes (not illustrative fragments), real authority/admission and v6 portability.
- Emit valid IK acceptance/final receipts and owner-preserving artifact-ready event using owner code.
- Ensure native connector is mockable; do not reinvent IK transport/delivery.

**Done when:** a source-owned export enters through a real IK test harness, Kristal-native fake sees the correct mapped shape, and outputs/receipts validate. A fake connector is **not** production proof.

## Milestone 3 — Reliable integration runner (P1)

- Add scoped idempotency and minimal process journal, with policy-controlled retention.
- Add bounded retry, timeouts, reconciliation and duplicate behavior.
- Add production-style security negative tests: tenant confusion, forged sender, tampered digest, SSRF, injection and log leakage.
- Instrument privacy-safe traces and structured errors compatible with IK.

**Done when:** crash/restart and duplicate tests pass; no unexpected business state or full source payload retained.

## Milestone 4 — Generic external capability (P1, requires IK ADR)

- Propose versioned IK Profile(s) for generic external admission that do not overload `kristal.build.request`.
- Define capability metadata with owner, required authority and output semantics.
- Integrate exactly one real non-Kristal capability from an external app with an approved owner connector.

**Done when:** source and receiver owners approve contracts, TCK passes C1–C4, and the foreign app's normal output is preserved and exchanged as intended.

## Milestone 5 — SDK, docs and qualification tooling (P1)

- CLI for validating profiles, contract pins and producing alignment reports.
- Templates for foreign app connectors and a minimal native-shaped external connector.
- Offline-friendly TCK test runner; signed/versioned report artifact if owner approves signing requirements.
- Guide for contributing adaptations without centralizing source owners' data.

**Done when:** a second developer can integrate a new fictitious external app following the guide without runtime-source edits or hidden hardcoding.

## Milestone 6 — Operational hardening / optional service (P2)

- Only if justified: hardened ingress process, host-level identity, deployment, rate limits and resilience.
- Independent security review, operator controls, telemetry and rollback.
- Clearly published compatibility table and lifecycle policy; optional public reports.

**Done when:** isolated integration environment, rollback drills, threat review and owner signoffs pass. Do not label production ready before these gates.

## Explicit exclusions from initial releases

No new semantic entity-resolution model, no self-service public API accepting arbitrary URLs, no direct student photo publishing, no scraping or source ingestion, no Orgo scheduler, no new IK event bus, no auto-training mapping AI, and no blanket v7/v8/v9/v10 artifact translation.

## Critical-path dependency map

```text
Contract owner decisions / pins
         |
  Mapping rules + TCK
         |
   IK v6 integration --------- Kristal v6 native port
         |
Security + idempotency
         |
Generic external IK profile (new owner ADR)
         |
SDK + external developer self-service
         |
Optional operational service hardening
```
