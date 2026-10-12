# Secure offline external mapping API

This API is a **local Python call**, not an IK profile, HTTP ingress or remotely callable system.

## Admission path

1. Host receives external data using an independently authenticated transport.
2. Host builds an `ExternalCall` with only bounded input and a *requested* mapping profile ID.
3. The trusted `ExternalIdentityProvider.verify` authenticates the external workload, separate actor, tenant and intended DaaT audience.
4. The trusted `SourceOwnershipVerifier.verify` checks source ownership and source content integrity.
5. The DaaT host-approved mapping allowlist locates the pinned profile; a caller cannot provide its own local path.
6. `SecurityGate` gets a fresh policy ALLOW, enforces its obligations and persists a minimal audit record.
7. The deterministic mapping runs within the configured 512-KiB JSON input ceiling (also configure process/network budgets externally); output is validated against the pinned target schema.
8. A second audit event precedes successful return. The result remains an in-process object; output delivery still belongs to approved owner interfaces.

## In-process integration sketch (not an HTTP deployment)

```python
from pathlib import Path
from daat.external import ExternalCall, ExternalMappingBoundary

boundary = ExternalMappingBoundary(
    authenticator=host_verified_workload_and_actor,
    source_verifier=host_source_integrity_verifier,
    policy=host_konfid_port, audit=host_trusted_audit_sink,
    allowed_profiles={
        'outside-inventory/1.0.0': Path('mappings/foreign-inventory/profile.json')
    },
)
result = boundary.map(ExternalCall(
    admission_ref='host-owned-attestation-id',
    claimed_system='outside-app', claimed_tenant='school-demo',
    profile_id='outside-inventory/1.0.0',payload=trusted_parsed_json_document,
))
```

The variables prefixed `host_` above are **mandatory owner implementations**, not packaged defaults. The sample does not create them or authorize traffic by itself.

## Zero transformation stays under security

The native identity profile (`native-export-identity/1.0.0`) has burden 0 for its declared field obligations, but cannot be executed without the exact same workload, actor, source verifier, policy and audit controls.

## Limits

- No arbitrary URL/file source fetching, profile path selection, dynamic mapping code, or invocation of a second mission/workflow engine.
- The input size ceiling is a **single local JSON value**, not a public traffic/DDoS guarantee; add host limits, rate limiting and concurrency budgets.
- Source checks and actor identity are implemented as **ports**, not cryptographic implementations.
- No IK external ingress profile is approved by this new class. The actual wire flow must await IK-owner agreement.
