# Operations, observability and rollback

## Default footprint

Ship DaaT first as **local library + CLI + IK integration adapter**, not a new online platform. A persistent service is an optional later deployment choice. Never presume public Internet exposure. Host, tenant and trust settings belong to the deployment owner.

## Observability model

Allowed structured fields: `interaction_id`, `correlation_id`, `receiver`, `profile_id/version`, mapping pack digest, target owner, tenant pseudonym or internal opaque ID, status, error code, duration, retry count and transform summary counts.

Disallowed by default: document bodies, credentials, student personal data, private artifact locators, unredacted foreign identifiers, protected knowledge content and owner-private policies.

Metrics:

- `admission_requests_total{profile,status}`;
- `mapping_failures_total{reason}`;
- `native_call_duration_seconds{capability}`;
- `receipt_delivery_failures_total` (if exposed by IK integration);
- `artifact_integrity_failures_total`;
- `alignment_reports_total{method_version}`;
- `unsupported_versions_total{profile}`;
- `replay_conflicts_total`.

Do not use highly cardinal labels such as student IDs, artifact IDs or raw tenant secrets.

## Alerts and actions

| Signal | Meaning | Action |
|---|---|---|
| Spike in unauthorized submissions | Threat or misconfiguration | Inspect issuer/audience/tenant, block if necessary |
| Digest mismatch | Tamper or stale pins | Quarantine, verify owner release |
| Mapping ambiguity surge | Changed foreign shape | Disable affected mapping version, request owner decision |
| Native call timeout/retry growth | Dependency incident | Rate-limit, recover via idempotency/correlation |
| Artifact output invalid | Semantic contract failure | Do not emit ready, owner escalation |
| Alignment burden suddenly drops | Could be true alignment or hidden transform | Compare actual fixture semantics and changed scope |
| Log leak | Privacy incident | Suspend risky logging, rotate credentials, follow owner incident plan |

## Change control

Pin mapping profiles immutably. Record source and target contract digests, capability scope and approval. Use staged canary against synthetic fixtures, then test owner environment, then broader rollout if authorized. A new mapping cannot silently replace an old version while durable operations remain in flight.

## Rollback

Rollback executable code and mapping profile **together** to a tested pair. Keep existing idempotency processing record so rollback does not replay effects. If source schema changed, rollback may be unsafe; stop and require a new mapped profile instead of lossy conversion.

## Failure recovery runbook

1. Identify `correlation_id`, profile, mapping pin and tenant scope from safe logs.
2. Verify current trust/authorization status before retry.
3. Determine whether native owner has acted using owner-native correlation.
4. If not acted and retryable, resume with same source snapshot/profile pin; if acted, reconcile and emit missing receipt rather than reinvoking.
5. Preserve owner artifact references and state.
6. Document incident and add negative fixture before reopening affected capability.

## Disaster recovery

Only journal metadata needs recovery. Source artifacts and Kristal materializations remain with their owners. Rebuild alignment reports from pinned contracts, fixtures and mapping manifests. Never advertise DaaT as a source data backup.
