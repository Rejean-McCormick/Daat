# Implementation status — v0.3.0, 2026-10-12

The v0.1 Markdown specifications remain design guidance; v0.3 now ships an **offline Python library/CLI with injected security enforcement**. This file supersedes earlier statements that the repository contains no code, but does not imply deployment readiness.

| Area | Real implementation | Evidence | Limit |
|---|---|---|---|
| IK owner schema verification | Yes | `daat verify-contracts`; pytest contract tests | Snapshot-pinned copies; never auto-upgrades |
| IK v6 command payload gate | Yes | `daat validate-build`; negative tests | Existing IK profile only; not generic IK admission |
| Mapping DSL | Draft implementation | `daat map`, golden tests | Local DaaT format unapproved as ecosystem wire contract |
| Alignment burden | Yes (declared scope) | CLI JSON reports + tests | Not independent upstream transformation audit; no badge |
| In-process build port | Testable with injected ports | Fake-native unit tests | No live IK or Kristal transport installed |
| Auth and authority | Fail-closed injection points | Cross-tenant and missing-trust tests | **No real cryptographic provider** |
| Artifact integrity | Fail-closed injected verifier | Negative/tamper tests | No fetching and no owner bytes verifier included |
| Replay | In-memory guard | Duplicate/conflict tests | No durable process restart/reconciliation; not exactly-once |
| Receipts/events | Owner-schema-valid record factories | Unit tests | No actual IK delivery, no final failure record on native exception |
| v7/v8/v9/v10 support | No | explicit warning | v7 design draft mismatch blocked |
| Host-backed Konfid policy PEP | Offline in-process code | `tests/test_security.py`, negative paths | No real authenticated Konfid RPC; kOA remains policy authority |
| External mapping boundary | Offline in-process code | Verified external test fixtures | No IK-approved general ingress profile or authenticated public service |
| Audit PEP | Minimal sink port | audit-failure security tests | No persistent owner Audit Broker deployed |
| Human or service actor | Mandatory verified actor in principal | actor-missing tests | Real OIDC/workload proof is host responsibility |
| HTTP / production | No | No HTTP process is shipped | Requires owner-approved deployment/security architecture |

## Known hard boundaries

1. `Interaction-Kernel` governs envelopes, profiles, events, delivery, correlation and wire codes. DaaT does not create a second event bus.
2. Real `kristal.build.request/2.0.0` profile allows `konnaxion` and `orgo`, not arbitrary external senders. Generic external profile needs an IK owner-approved contract and release.
3. The local declarative `daat.mapping-profile/0.2.0-draft` is a **draft file format for an offline tool**, not an approved externally negotiated capability.
4. Kristal `6.0.0` portable build is pinned; no silent equivalence with later layer drafts.
5. External manifest integrity and authentication require independent host and owner verifiers. Fake ports used in tests must never become a public endpoint's defaults.
6. Before a beta release, verify wheel packaging, operator recovery, real owner TCK integration and upstream licensing.

## Release qualification

Current state: `security_boundary_alpha` plus an **in-process synthetic IK/native interaction**. Track C4 in `docs/09-CONFORMANCE-AND-TESTS.md` is **not passed**, as it requires running real owner integrations. No production certification is claimed.

## v0.3 security implementation summary

The policy enforcement gates in `src/daat/security.py`, `src/daat/konfid_port.py` and `src/daat/external.py` are implemented and covered by synthetic tests. They are **not** a live Konfid/Kristal/IK deployment. The policy callback, identity providers, output verifier and audit sink must be supplied by separately reviewed host code. See [security](20-SECURITY-BOUNDARY.md), [Konfid alignment](21-KONFID-CONTRACT-ALIGNMENT.md) and [threat model](23-THREAT-AND-TRUST-MATRIX.md).

## Local demo

`python examples/fake_host_demo.py` exercises only a synthetic owner build client and fake trust providers. It is useful to inspect receipt and event shapes, but passing it **does not** satisfy C4 real integration conformance.
