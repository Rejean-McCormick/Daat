# 32 — Threat model, contract TCK and qualification matrix

**Status:** `TARGET_DESIGN`; supplements the existing [09 conformance](09-CONFORMANCE-AND-TESTS.md) and [23 trust matrix](23-THREAT-AND-TRUST-MATRIX.md). It does not claim that these tests already exist or passed.

## 1. Tiered evidence policy

| Tier | Meaning | May be claimed when |
|---|---|---|
| **T0: Specified** | Source/target responsibilities and contracts recorded | Reviewed docs, no operation claim |
| **T1: Offline fixture-tested** | Mapping/extractor tests run locally with fake ports | Exact source revision, tool versions, commands and outputs recorded |
| **T2: Owner contract-tested** | Real owner schemas, TCK and permission PEP tested | Both sides pin exact versions and valid/invalid samples |
| **T3: Bilaterally integrated** | Real source/custody/IK/Kit endpoints and terminal receipts proven | Owner-qualified runtime evidence, denial and crash recovery |
| **T4: Operationally qualified** | Production-like deployment, rights, security, recovery, observability approved | Independent validation and deployment owner sign-off |

Do not elevate T1 to T3 on the strength of a schema-only test or mock. These tiers are **documentation conventions**, not new public certification authority.

## 2. Required negative tests by boundary

| Threat/failure | Injection | Expected invariant |
|---|---|---|
| Forged principal/workload | Caller-provided identity fields, wrong token binding | Deny; trusted host verifier required |
| Cross-tenant confusion | Valid source ID but wrong tenant/library instance | Deny without exposing source bytes |
| Unauthorized scope | API token lacks export/read grant, expired source rights | Stop before fetching/disclosing data |
| Unapproved IK profile | Generic JSON sent as `kristal.build.request/2.0.0` | Deny; never repurpose approved profile |
| Integrity mismatch | Mutated byte/blob after approved hash | Deny with no downstream effects |
| Unknown profile/version | Different mapping/owner schema/draft | Deny; no silent fallback |
| Loss of mandatory meaning | Debit/credit sign lost, timestamps truncated, `unknown` coerced to false | Reject transform, explicit loss report |
| External identity smuggling | Wikidata Q/P mislabeled KQ/KP | Candidate only, not accepted canonical identity |
| Prompt injection | PDF/README instructs agent to leak keys or change policies | Treat as data, never command authority |
| Unsafe parser/archive | Nested ZIP bomb, HTML SSRF, XXE, path traversal, malicious macro | Sandbox/size limit; deny or quarantine under custodian control |
| Confidential output | PII or secrets in logs/fixtures/telemetry | Redact/minimize and test leak detection |
| Duplicate/replay | Same key changed request digest; stale checkpoint | Reject conflicting replay; idempotent same-intent behavior |
| Partial/unknown side effect | Receiver times out after possible write | Enter reconciliation; no blind resubmit |
| Unavailable Konfid/audit | Policy or audit callback failure/stale ALLOW | Fail closed; no allowed-by-default path |
| License denial | Terms forbid full-text rehosting or bulk corpus mirror | No copy; reference-only if independently allowed |
| Canonical laundering | AI extraction output labeled `validated`, `recognized`, `published` | Block until exact semantic/authority gates |
| Release escalation | Valid local build used as public publishing authorization | Deny without independent qualification and owner consent |
| Revocation and retention | Tenant withdraws source access | No new reads; apply owner-approved lifecycle to cached evidence |

## 3. Test harness contract

Every pilot profile needs:

- **Positive:** sanitized golden input and exact expected output; source and target schemas pinned; stable digest and source citations.
- **Negative:** invalid/missing/extra fields, unknown and nullable semantics, loss of qualifiers, mismatched integrity, malicious untrusted content and inaccessible source.
- **Authorization:** authenticated actor/workload, purpose, tenant, scopes, decision expiry and audit availability; known-good test principal must be explicitly fake.
- **Isolation:** secrets do not cross worker/tenant; Annex has no write/publish privileges.
- **Replay:** identical snapshot/transform equals stable output; changed input or transform is a new immutable revision; same idempotency key with different intent fails.
- **AI:** same claimed source location verifiable; uncertain model recommendation doesn't bypass deterministic admission; prompt injection does not become instructions.
- **Owner effect:** producer and consumer observe compatible terminal outcomes; internal mock receipts cannot substitute for live IK.
- **Lifecycle:** correction, cancellation, revocation, archive and rollback paths tested for source/custody/authoring ownership.

Record command lines actually executed, exact code/dependency digests, test environment, failures, unresolved security questions and owner approvals. Automated acceptance must not assert `SUPPORTED` when no adopted owner interface exists.

## 4. Reproducibility and evidence manifest

For every test run publish a **test-evidence report** (within allowed security scope) with repository commit, source fixture digest, adapter and mapping versions, target schema and IK pins, test command/result, environment, owner sign-off and date. A report is local engineering evidence, **not** a Kristal signature, release right or new proof of factual knowledge.

## 5. Security gates before an external runtime

- Adopted owner-controlled ingress profile and actual authenticated trusted host.
- Tenant/service principal authentication and actor binding; approved Konfid transport/PEP/audit integration.
- Bounded source resolution and credential storage outside DaaT; privacy and retention policy.
- Durable idempotency, outbox, crash recovery and reconciliation for side-effect-bearing operations.
- Parser/connector sandbox, egress policy, file type/size guards, runtime resource limits.
- Independent integration and threat review plus legal check of code/data licenses.

Until then the existing **offline v0.3 library and synthetic ports remain non-production**.

**Owner refs:** [AGENTS rules](../AGENTS.md), [19 — Status](19-IMPLEMENTATION-STATUS.md), [20 — Security](20-SECURITY-BOUNDARY.md), [21 — Konfid](21-KONFID-CONTRACT-ALIGNMENT.md), [23 — Trust matrix](23-THREAT-AND-TRUST-MATRIX.md).
