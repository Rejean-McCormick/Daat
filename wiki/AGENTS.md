# AGENTS.md — Build contract for AI implementers

This file is binding implementation guidance for code-generation agents working in DaaT. It is **not** a substitute for an approved release or security review.

## 0. Status discipline

Use these tags in design/PR notes: `[UPSTREAM-FACT]`, `[OWNER-DECISION]`, `[PROPOSAL]`, `[BLOCKED]`, `[TESTED]`. The source snapshot facts are listed in `docs/01-SOURCE-BASELINE.md`. Proposed DaaT-generalization rules do not supersede accepted IK/Kristal ADRs. If a conflict is found, **stop the affected feature**, document it, propose a versioned contract change and continue unrelated work.

## 1. Absolute rules

1. NEVER create a second event bus, mission scheduler, workflow engine, semantic identity authority or artifact store.
2. `daat` is the machine system ID; `DaaT` is the human name. Do not rename existing IK profiles or canonical IDs.
3. No silent schema coercion, identity equivalence, epistemic upgrade, version fallback, or auto-granted authorization.
4. A zero-semantic-transform adapter still requires authentication, authorized admission and schema validation where the relevant boundary requires them.
5. All mappings MUST be declared, versioned, integrity-pinned, deterministic for the same pinned input/config, and independently tested.
6. Preserve original artifact owner; DaaT never claims custody/authority merely by forwarding an ArtifactRef.
7. Fail closed on invalid profile, untrusted identity, policy denial, integrity mismatch, unsupported version, unknown transformation, or loss of a required semantic field.
8. Do not map an external ID into Kristall KQ/KP/KA/KS without Kristal-owned authority/contract. Preserve it as an external identifier or candidate.
9. Never log credentials, source bytes, private student data, or full sensitive payloads.
10. No remote code execution via mappings (`eval`, dynamic imports, unsafe plugins, user-authored scripts). Prefer a declarative, allowlisted mapping DSL.
11. Do not infer source-owner mutation rights from Kristal `actionability.mode=automatic`.
12. Never mark a feature `implemented` because its schema, mock, sample or documentation exists.

## 2. Authority boundaries

- IK: envelopes, profiles, routing/delivery and receipts.
- Kristal: portable knowledge schema, semantic identities and semantic validation/recognition.
- Orgo: process/task state and its transitions.
- Other systems: their own operational data, access policies and secrets.
- DaaT: explicit mapping/admission edge only. It may record **minimal integration operational metadata** for reliable processing; this is not source/business state or semantic authority.

## 3. Source-of-truth rules

Read these upstream files, not this document alone:

- `Interaction-Kernel/interaction_kernel/docs/adrs/ADR-IK-07-daat-kristal-v7-boundary.md`
- `Interaction-Kernel/interaction_kernel/docs/kristal-daat.md`
- `Interaction-Kernel/interaction_kernel/adapters/daat/README.md`
- `Interaction-Kernel/interaction_kernel/contracts/schemas/envelope.schema.json`
- `Interaction-Kernel/interaction_kernel/contracts/schemas/artifact-ref.schema.json`
- `Interaction-Kernel/interaction_kernel/contracts/profiles/kristal/kristal.build.request/2.0.0/`
- `Kristal-Framework/spec/v7/DaaT-Boundary.md`
- `Kristal-Framework/spec/v7/00-overview/specification-status.md`

File paths above use snapshot-relative prefixes; discover the actual checkout roots rather than assuming nested directory names.

## 4. Implement in this order

1. Contract baseline checker + fixture validator, with exact pin checks.
2. Pure alignment evaluator that reads contracts/mapping declarations without network access.
3. Mapping validator and mapping engine with no ad hoc `if app == X` conversions.
4. In-process IK admission client port and signed/authorized receipt handling using existing IK owner code.
5. Reliable process journal and idempotency (only if durable service mode is chosen).
6. V6 build reference integration with a fake Kristal client and contract TCK; then native client integration.
7. External integration templates and CI-generated alignment reports.
8. Optional HTTP service **only after** agreed deployment/security model and acceptance tests.

## 5. Definition of done for each PR

- Precise upstream version/pin listed.
- Valid fixture and at least one invalid/malicious fixture.
- Unit tests for normalization, integrity, scope and idempotency where relevant.
- No hardcoded credentials or production URLs.
- Failure and recovery path documented.
- Contract shape checked using the real owner schema, not an invented approximation.
- No existing upstream snapshot or contract modified without a separate approved change.
- Security/privacy test for new artifact/log surface.
- Reproducible output and file hashes for published alignment reports.
- Documentation explains what remains untested in production.

## 6. Required deliverables

When implementing a milestone, provide: changed files, commands actually run, test output summary, link to fixture, open decisions, compatibility baseline and a short risk review. Do not announce end-to-end readiness when only tests/mocks pass.

## 7. Stop conditions for agents

If upstream v6/v7/v8/v9/v10 contracts conflict, a receiver's authorization policy is unknown, tenant identifiers cannot be established, a source field has no safe lossless mapping, or a new IK Profile is needed but unapproved: write an ADR/question and stop that path. Do **not** improvise an API or semantics to make the demo pass.

## 8. v0.3 security invariants (code exists; production provider does not)

- `SecurityGate` is an enforcing PEP, **not** Konfid, an IdP or the kOA PDP.
- Every owner build needs both verified workload and actor (human assertion or trusted service principal), scoped capability, exact-bound fresh policy ALLOW, source integrity and auditable outcome.
- Konfid `AccessRequest` fields are preserved; `KonfidPolicyPort` is NOT proof of secure network transport. The host must provide issuer/audience/jti checks, actor azp-client binding, workload credentials, transport security, and authoritative policy decision provenance.
- Reject unrecognized obligations, missing decision validity, unknown/overlong ALLOW, unavailable policy/audit, unauthorized profile, cross-tenant artifacts and stale replays.
- `ExternalMappingBoundary` has **no IK transport profile**. Never expose it directly as an HTTP handler until IK formally owns and approves the external ingress profile and runtime TCK passes.
- Failures after a native side effect keep an uncertain journal state; do NOT blindly retry. The included memory journal is test-only; production requires durable idempotency, outbox and reconciliation.
- A smaller semantic adapter does not remove identity/policy/audit enforcement.
- Test-only providers in `tests/` and `examples/fake_host_demo.py` must never be used in a deployed process.

## Current implementation note (v0.3.0)

The offline Python CLI/library and in-process security gate are implemented and must pass `python -m pytest -q`. Review `docs/19-IMPLEMENTATION-STATUS.md` before claiming readiness. The new mapping draft is not an approved IK wire profile; all real trust and external transport decisions remain blocked.
