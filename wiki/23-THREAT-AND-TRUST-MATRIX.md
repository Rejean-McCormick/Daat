# Security threat matrix and ownership

| Threat | Local DaaT v0.3 control | Mandatory host/owner control | Evidence |
|---|---|---|---|
| Forged workload / actor | Reject absent or untrusted `VerifiedPrincipal`; require explicit actor, audience `daat` | Cryptographically validate IdP, service JWT, actor assertion/azp, issuer, audience, jti, expiry | `tests/test_bridge.py`, `test_security.py` |
| Cross-tenant forged source | Check trusted principal matches IK source / external source, owner/tenant on artifacts | Tenant-aware owner storage lookup, resource authorization | `test_cross_tenant`, `test_external_identity_tenant_mismatch_fails` |
| Confused deputy through URL | Opaque URN reference in v6 build; no URL fetcher | Owner-defined retrieval; SSRF and metadata-network restrictions | `test_malicious_locator` |
| Unapproved profile | Exact DaaT allowlist ID plus pins | Admin-reviewed mapping deployments and signed registry where needed | `test_external_unapproved_profile_fails` |
| Permit/replay misuse | Fresh, short-lived bound policy decision every time, even cached success | Authenticated policy transport and enforced revocation/expiry | `test_replay_reauthorized_after_policy_revoke` |
| Unknown obligations | Deny unknown types; reject `no_export`; enforce `max_rows` | Policy owner evolves obligations via tested contract changes | `test_policy_negative_paths` |
| Forged policy provenance | Requires trusted policy port and request binding | TLS/mTLS, issuer/authority proof; no untrusted callable in production | Synthetic ports only; **no actual cryptographic test** |
| Missing audit / lost evidence | Audit sink required; unavailable sink blocks effects | Durable kOA Audit Broker, chain validation, no private payload | `test_unavailable_audit_fails_closed` |
| Duplicate native side effect | Memory in-doubt journal prevents blind second invocation | Durable transactional outbox, idempotent native owner, reconciliation | `test_audit_failure_after_effect_requires_reconciliation` |
| Stale schema/version | Digest pinned owner schemas and mapping references | Signed/reviewed release-set admission | `test_contracts.py`, `test_mapping.py` |
| Oversize input | 512 KiB JSON cap in external API | Transport body limits, concurrency and execution timeouts | `test_external_large_input_rejected` |
| Student/privacy leak | No student data in reports, minimal `AuditRecord` fields | Data-owner consent, retention, encryption, rights review, redaction | Design only; **not validated with real data** |
| Supply-chain compromise | Minimal package dependencies, owner contract digests | SBOM, provenance and independent release gate | Build + package tests; no signed provenance |

### No production claims

This release cannot attest to real OIDC/JWT verification, live policy and audit, deployment firewall, real artifact digests or native Kristal correctness. All synthetic actors, policy responders and integrity verifiers in tests/examples are explicit fakes.
