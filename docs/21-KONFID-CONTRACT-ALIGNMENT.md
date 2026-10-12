# Konfid and kOA contract alignment (source-preserving)

The provided Konfid snapshot has `AccessRequest`, `ResourceRef`, `AuthorizationContext`, `AccessResponse`. DaaT does not introduce a competing policy schema.

| Owner field | DaaT mapping | Trust origin |
|---|---|---|
| `request_id` | `DAAT-` + bounded request binding | DaaT computes from canonical exact intent |
| `tenant` | `PolicyRequest.tenant` | Host-verified workload/actor tenant |
| `actor` | `PolicyRequest.actor` | Host-verified human assertion or workload service principal |
| `action` | `kristal.build.request` or `daat.mapping.execute` | DaaT typed operation, not caller-selected elevated action |
| `resource.owner` | `kristal` or `daat` | Local bridge type / approved profile |
| `resource.class` | `kristal_build` or `mapping_profile` | Local known resource class |
| `resource.selector` | Owner IK request ID or exact pinned DaaT profile ID | Matched to owner-validated input |
| `scope.caller_service` | authenticated calling system | Host workload identity |
| `scope.intent_sha256` | canonical action/request digest | DaaT local hash; no raw payload in the access request |
| `context.auth_assurance`, `auth_age_seconds` | independently verified actor assertion | Host identity adapter |
| `context.requested_count` | owner artifact count | Validated locally; policy may narrow with `max_rows` |
| `context.purpose` | specific operation purpose | Local operation binding |

Konfid response (`decision`, `decision_id`, `policy`, `valid_until`, `obligations`, `reason_codes`) is parsed by the host-supplied trusted policy port. DaaT binds it **locally** to the call being evaluated, then rejects deny, missing/expired expiry, unknown obligations and policy outage. DaaT's local `BoundDecision.binding` is **not an extra Konfid wire field**; a production host must securely establish that the response corresponds to the requested call.

**Owner gap:** the provided Konfid `AccessResponse.valid_until` is optional. In v0.3 DaaT requires an explicit short expiry for ALLOW. Owners must coordinate if actual policy runtime produces an ALLOW with no expiry. No permissive fallback is installed.

**Authorization ownership:** Konfid maps identities and accesses; kOA Governance Policy Runtime is the production PDP when enabled; kOA Audit Broker receives authoritative evidence. IK transports accepted interactions. DaaT never writes Konfid grants, kOA policy, Orgo task state or Kristal semantic decisions.

**Operational gap:** `KonfidPolicyPort` is a pure injected adapter, **not** a production authenticated HTTP client. The supplied Konfid archive's transport expectations (bounded TLS, optional mTLS, short workload/actor JWT, timeouts, fail-closed on kOA outage) must be fulfilled by the host integration.
