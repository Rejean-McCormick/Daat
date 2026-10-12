# Runtime lifecycle, delivery and failures

## Scope

The baseline IK `kristal.build.request/2.0.0` profile is durable, idempotent and requires acceptance and final receipts; output event is `kristal.artifact.ready/2.0.0`. DaaT **must reuse IK wire and delivery semantics**. A generic external-adapter profile needs a separately approved IK capability/version.

## Proposed processing state machine

```text
RECEIVED
  | parse/schema/authn/authz/profile/pin gate
  +--> REJECTED (terminal; no native invocation)
  +--> BLOCKED  (terminal or explicit remediation; no unauthorized work)
  v
ADMITTED -> ACCEPTANCE_RECEIPT -> MAPPING -> NATIVE_INVOKE
                                              |            |
                                              |            +--> RETRYABLE_FAILURE
                                              v
                                         OUTPUT_VERIFY
                                              |
                          +-------------------+----------------+
                          |                                    |
                          v                                    v
                    FINAL_SUCCESS                         FINAL_FAILURE
                          |
                          v
                 OWNER_REF_EVENT / RECONCILE
```

`RECEIVED`, `MAPPING` etc. are **internal implementation states**, not new IK Receipt status values. IK receipt schema currently enumerates `accepted`, `rejected`, `blocked`, `succeeded`, `failed`. Emit only owner-schema statuses on IK.

## Deterministic identity and idempotency

Proposed idempotency scope:

```text
(receiver instance, verified sender identity, tenant,
 profile ID/version, idempotency_key, exact request digest)
```

- Same key/same digest: return recorded outcome or resume safely.
- Same key/different digest: reject as `IDEMPOTENCY_CONFLICT`; no fresh action.
- Journal only minimal digest, mappings and refs; never unredacted source bytes.
- Native connector must support owner-issued idempotency/correlation where possible; otherwise do not claim exactly-once effects.

## Receipts and events

Use IK owner schemas. For build command:

- acceptance receipt after valid admission and before native side effects;
- final receipt with success/failure, diagnostic code, retryable flag, correlation;
- artifact-ready event for verified finished artifacts with owner-preserving `ArtifactRef`;
- never emit `reference` merely because an artifact compiled. Preserve Kristal validation/recognition stages.

The receipt schema's fields `status`, `retryable`, `code`, `external_reference` and `data` must be respected. Message ordering should not be assumed (`ordering: none` in IK Profile). Correlate with stable IDs rather than relying on arrival order.

## Failure taxonomy (PROPOSAL, map to existing IK catalog before coding)

| Error | Retry? | Operational response |
|---|---|---|
| `SCHEMA_INVALID` | no | Reject with field/path diagnostics safe for sender |
| `UNKNOWN_PROFILE` | no | Reject, list compatible profiles if allowed |
| `UNSUPPORTED_CONTRACT_VERSION` | no | Reject, require new approved version |
| `AUTHENTICATION_FAILED` | no | Reject/blocked, avoid disclosing tenant existence |
| `AUTHORIZATION_DENIED` | no | Block |
| `ARTIFACT_INTEGRITY_FAILURE` | no | Reject/quarantine, do not invoke native |
| `MAPPING_AMBIGUOUS` | no | Block pending owner review |
| `MAPPING_LOSS_FORBIDDEN` | no | Reject |
| `NATIVE_TEMPORARY_UNAVAILABLE` | yes | Bounded exponential backoff with jitter and circuit breaker |
| `NATIVE_REJECTED` | depends | No retry if semantic/policy failure |
| `OUTPUT_INVALID` | no/owner decision | Quarantine output ref, report defect, do not publish as ready |
| `IDEMPOTENCY_CONFLICT` | no | Reject |

Before implementation, reconcile proposed codes with `Interaction-Kernel/contracts/errors/error-catalog.json`; prefer existing code names where defined.

## Timeouts and recovery

- Distinct deadlines for admission, mapping and native invocation.
- Cancel/timeout never implies that a remote native operation was undone.
- Reconcile by querying owner-native operation ID/correlation; avoid duplicate mutations.
- Dead-letter handling belongs to IK/delivery infrastructure as appropriate, not a new independent queue.
- Reprocess with same mapping pin and source revision; a new mapping version is a **new operation**.

## Operational state journal

A local durable journal is allowed for `request_id`, verified sender/tenant, digest, mapping pin, idempotency, status, receipt and output refs, timestamps and retries. Disallow source documents, student records and full normalization outputs as journal data.

## Required failure tests

Malformed envelope; wrong target; no auth; cross-tenant access; unknown pin; tampered source digest; missing required mapping; timeout before and after native side effect; duplicate command; duplicate outcome event; unordered receipts; out-of-order artifact reference; invalid output; rollback with pinned mapping from previous release.
