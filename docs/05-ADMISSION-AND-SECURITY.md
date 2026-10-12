# Admission, authorization, trust and privacy

## Security principle

**Schema alignment is not trust. Authentication is not authorization. Transport admission is not semantic validation. A signature is not epistemic recognition.** Maintain these separations even in the zero-transform adapter.

## Processing gates, in order (PROPOSAL)

1. **Parse safely:** limit size, depth and document counts before heavy parsing; reject unknown encodings where disallowed.
2. **Validate transport envelope:** exact IK owner schema and version; reject wrong classes/profile/target.
3. **Authenticate sending system:** configured trusted identity, key or OIDC assertion via IK/host authority; verify issuer, audience, expiry and intended recipient as applicable.
4. **Authorize operation:** scoped to system, capability, tenant, subject, artifact type and requested output. DaaT cannot grant owner-level rights by itself.
5. **Verify profile, lock and digests:** exact declared versions and pinned schema/content hashes.
6. **Verify source owner/capability:** exported ArtifactRefs/ExportManifests have owner and integrity; restrict locators to allowed transports and address spaces.
7. **Validate input + declared mapping policy:** required fields, explicit loss policy, approved transformation pack.
8. **Execute deterministic mapping:** resource limits; no network fetching through a mapping expression.
9. **Validate native output:** via owner validators, including any required source/provenance/Reader Policy semantics.
10. **Emit receipt/event:** owner-preserving `ArtifactRef`, proper status, no sensitive payload in observability.

Where IK is responsible for some checks, DaaT verifies the evidence of admission and still enforces its local receiver boundary; it must not invent a second independent identity registry.

## Threat model

| Threat | Required prevention / test |
|---|---|
| Forged envelope/source | Verify sender cryptographically via real host/IK policy; schema alone never enough |
| Confused deputy | Verify recipient, target, audience, tenant and requested capability; no authority transfer by mere forwarding |
| Tampered artifact | Verify digest and owner binding before use |
| SSRF / path traversal | No arbitrary URL/file read from `ArtifactRef.locator`; allowlist transport, host, root paths; deny metadata/private networks |
| Mapping code injection | Declarative restricted transform operations, no `eval` or arbitrary dynamic imports |
| Schema downgrade | Unknown/older pins fail closed, no auto-fallback |
| Cross-tenant disclosure | Strict tenant partitions for cache, journal, responses and diagnostics |
| Replay / duplicate effects | Idempotency key + stable replay outcome |
| Denial of service | Size, rate, concurrency, deadlines and memory limits before mapping |
| Sensitive logs | Safe structured logs without payload, credentials, full identifiers or personal artifacts |
| Semantic privilege escalation | No change to validation/recognition/actionability without domain authority |
| Supply-chain manipulation | Pinned reviewed mapping packs and reproducible fixtures |

## Student data and sensitive educational content

DaaT may connect to Ekole indirectly, but educational artifacts can include children's data. Default policy: **no student records in public fixtures or alignment reports**. A DaaT mapping cannot publish images, names or tags without an explicit owner-controlled publication authorization. A denial results in no public artifact or identifying reference. Redaction of logs is not sufficient privacy protection if an accessible URL still points to the data.

## Secrets and key handling

- Do not put secrets in JSON mapping profiles, docs, CLI output or Git commits.
- Use an approved secret store/environment injection mechanism; document rotation and revocation.
- Do not log raw bearer tokens or customer credential filenames.
- Do not embed credentials in artifact locators.

## Authorization failure semantics

- Unknown identity, insufficient scope, mismatched tenant or untrusted artifact: **reject or block**; do not attempt a semantic mapping.
- No fallback to 'best effort' privilege.
- Notify via IK-conformant rejected/blocked receipt if authorized to respond, avoiding existence leaks.
- Record minimal audit metadata: profile, correlation, outcome/error code, mapping pin, subject hash or non-sensitive ID, time.

## Data retention

Processing metadata retention should be minimal and policy-configured. DaaT must not become a shadow warehouse: no long-lived external source bytes, no complete uploaded documents as journal entries, and no persistent normalized copy unless the owner has an explicit distinct storage contract.

## Security exit criteria

A milestone cannot be called complete before: forged sender rejected; unauthorized tenant rejected; malicious locator rejected; duplicate operation safe; payload exfiltration/logging test passed; map injection rejected; integrity failure rejected; no silent semantic status upgrade.
