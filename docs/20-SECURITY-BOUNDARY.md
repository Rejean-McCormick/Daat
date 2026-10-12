# DaaT security boundary — implemented design and upstream obligations

**Status:** local code implemented in v0.3.0; owner service deployment **not implemented**. This document does not certify security or replace Konfid/kOA policy and audit.

## Security boundary vs semantic compatibility

DaaT is a controlled **external integration PEP**. An aligned external client has a zero semantic-transformation burden but still passes identity, actor, policy, provenance, mapping-contract, and minimal audit checks. Security assurance is **not** a component of the semantic alignment burden score.

```
Untrusted external source
    -> host authentication (workload + bound actor assertion)
    -> DaaT input/provenance/contract gate
    -> trusted Konfid EvaluateAccess / kOA policy decision
    -> DaaT PEP verifies precise bound decision and obligations
    -> approved deterministic mapping or v6 build (only)
    -> domain-owner authority / IK transport (external to this library)
    -> trusted owner Audit Broker (host implementation)
```

The DaaT library never obtains standing credentials to operate as an administrator. A Konfid ALLOW is a *necessary but insufficient* condition: Kristal, IK or Orgo must still enforce their own resource invariants.

## Executable ports

- `PolicyRequest`: tenant, independently authenticated caller, independently verified actor, operation, resource owner/class/selector, SHA256 of exact intent, requested item count, purpose and assurance context. Host must **not** derive caller or actor from untrusted body fields.
- `SecurityGate.authorize`: validates returned `BoundDecision` binding, exact `ALLOW`, nonempty policy provenance, UTC expiry no greater than 120 s, and all returned obligations. A missing, malformed, denied, expired or unknown response blocks execution.
- `KonfidPolicyPort`: converts the `PolicyRequest` into the **existing** Konfid `AccessRequest` (`actor`, `tenant`, `action`, `resource`, `scope`, `context`). Host-injected trusted call returns existing `AccessResponse`, to which DaaT adds a local immutable binding to the request just sent. The host MUST verify response source and transport. Merely passing a Python callback does not make it trustworthy.
- `AuditSink`: must commit a payload-free `AuditRecord` to a trusted durable audit facility. The shipped fake sink is used only in tests. Audit outage blocks subsequent side effects.
- `ExternalMappingBoundary`: accepts only operator-configured profile IDs, verified source provenance, verified workload and actor, policy and audit. No free-form file path, URL, plugin, code execution, or live network endpoint.
- `V6BuildBridge`: checks the approved owner IK v6 build profile and artifacts, authorizes the exact request **before any native effect**, re-authorizes cached replays, validates outputs, commits audit before recording success.

## Konfid obligations recognized by reference PEP

- `max_rows`: positive or zero limit; request count cannot exceed it.
- `no_export`: **deny** on DaaT mapping/build; no special escape path.
- `audit`: `basic`, `standard`, `enhanced`, `full` levels accepted as recognized. Actual level-specific persistence remains host responsibility; without an owner-specific attested audit sink no deployment is permitted.
- `authority_source`: metadata; validated but does not grant new authority.
- Any other obligation: **reject**. Adding a new obligation requires owner review and a unit/negative test.

**Important:** Konfid's current `AccessResponse.valid_until` is optional. For DaaT, an ALLOW without an expiry is **insufficient** and must be rejected. Agree and test policy TTL behavior with the Konfid/kOA owner rather than creating an implicit local ALLOW.

## Identity binding

Konfid documentation differentiates the workload identity and the human assertion. Human federation uses `issuer + sub`, not email. Workload JWTs require issuer, audience, short expiry and jti. Human actor assertions are separately verified and bound to caller via `azp/client_id`. DaaT does **not** implement JWT or OIDC, and the host must validate these before constructing `VerifiedPrincipal`. Pure machine operations require an authenticated **service principal as actor**, not a fabricated human.

## Resource failure and replay behavior

- Memory-only journal: test/dev use only. Repeated successful operation returns result only after a **new policy decision**; otherwise denied.
- On native or audit failure *after native effects might exist*, keep the journal in the uncertain state; reject the retry pending owner reconciliation. Never claim exactly-once based on an in-process dict.
- No IK receipts are emitted on the network by this library. `Outcome` contains owner-schema-valid **records** only; delivery belongs to IK and production durable outbox.
- A failed policy check before native execution must perform no build effect; tests assert this.

## Safety checklist before a real deployment

1. Have an IK-owner-approved generic external ingress profile, or use only the approved specific v6 build profile.
2. Bind authenticated workload and verified actor to tenant, exact action and target; separate machine from human identity.
3. Provide independently verified source ownership, bytes, digests and approved locator resolution; never fetch arbitrary URLs.
4. Integrate authenticated Konfid/kOA policy RPC with timeouts, circuit breakers, no unsafe fallback, clear ownership of response validity.
5. Integrate authoritative, durable, privacy-safe audit. Define persistence guarantees and outage behavior by operation type.
6. Implement rate budgets/concurrency controls at the host/network boundary, plus durable idempotency/outbox and crash recovery.
7. Run owner contract TCKs, cross-tenant adversarial tests, release gate via independent diagnostic and security review.
8. Define retention, user consent and child data-specific controls with data owners. No real student records in this alpha.

## Basis in provided archives

- `Code_snapshot_Konfid.zip`: `konfid/docs/ARCHITECTURE.md`, `AUTH.md`, `INTEGRATIONS.md`, `schemas.py` (AccessRequest/AccessResponse), `adapters/policy.py`.
- `senior-security-patterns.zip`: SEC-07 PEP/PDP separation, SEC-09 confused deputy, selective fail-closed, short-lived identity and signed delegation.
- `senior-architecture-patterns.zip`: anti-corruption layer, idempotency, timeouts and circuit breakers.
- The pinned owner IK and Kristal v6 materials under `contracts/owners/ik/`.

Those are source-derived constraints. The new `SecurityGate` API and 120-second TTL policy are **DaaT design decisions**, not existing owner-mandated contracts.
