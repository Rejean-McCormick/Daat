# Contracts, naming, compatibility and release rules

## Mandatory existing baseline (SOURCE)

- IK envelope/receipt spec: `ik/1.1` (schema owner: Interaction Kernel).
- Existing build command Profile: `kristal.build.request/2.0.0`, IK target system `daat`, capability `kristal-build`.
- Existing build data fields: `mapping_profile` (string), `requested_outputs` (nonempty string array), `kristal_contract_set` (exactly `6.0.0`).
- Existing event Profile: `kristal.artifact.ready/2.0.0`, sender `daat`, with `build_ref` and `stage`.
- IK build requires source exports, authority, idempotency, durable delivery and both acceptance/final receipts.
- Source-owned exports are described using `ExportManifest`; artifacts use `ArtifactRef` with **owner** separate from `artifact_id`.
- Portable Kristal contract is `kristal_state/6.0`; an additive v7 design does not rewrite it.

These are **owner-owned contracts**. DaaT repository may distribute links + pinned copies for offline test use, but must not publish its own incompatible copy under the same names.

## Illustrative command fragments — NOT a full IK envelope

```json
{
  "profile": {"id": "kristal.build.request", "version": "2.0.0"},
  "target": {"system": "daat"},
  "data": {
    "mapping_profile": "source-a-to-kristal/1.0.0",
    "requested_outputs": ["kristal_state"],
    "kristal_contract_set": "6.0.0"
  }
}
```

**IMPORTANT:** Above is a *fragment*. A real IK envelope requires `specversion`, `id`, `class`, `time`, `source`, `subject`, and other conditions imposed by the chosen profile. Validate real emitted envelopes against IK's exact `envelope.schema.json` and profile; do not copy this fragment as a complete wire example.

## Contract reference policies

1. Every mapping pack declares `source_contract_ref`, `source_digest`, `target_contract_ref`, `target_digest`, mapping version and transformation inventory.
2. Digests refer to **the exact bytes** defined by the contract owner; use the owner's canonical hash policy for semantic objects, not a random JSON reserialization.
3. Unknown major versions block the conversion; minor/patch support is explicit in a compatibility manifest, not assumed.
4. Changes to meaning, authority, mandatory fields or irreversible serialization require a new versioned mapping contract and new fixtures.
5. New IK capability/profile for non-Kristal external integration must be agreed with IK; DaaT must not overload the existing build profile.
6. Never silently rewrite third-party timestamps, actor IDs, tenant IDs, source evidence IDs or ownership claims.
7. Deprecation needs dual-read support only if a documented policy authorizes it, with a sunset date and no silent fallback.

## Proposed DaaT-owned metadata contracts (PROPOSAL)

These are documentation targets, **not shipped schemas yet**:

- `daat.mapping-profile/1.0.0`: input/target contract pins, safe operations, per-field rules, preservation and loss policy.
- `daat.alignment-report/1.0.0`: measurable differences, profile coverage, TCK result and normalization method.
- `daat.integration-capability/1.0.0`: supported external app, versions, operations, tenants and trusted endpoints; sensitive fields in private config.
- `daat.processing-record/1.0.0`: idempotency, correlation, status, profile pin, output ref and error code (private operational record, not IK replacement).

Contracts live under `contracts/` only **after** a separate ADR approves exact JSON Schema field naming. Avoid inventing a vaguely compatible wire standard inside DaaT.

## Compatibility matrix to maintain in CI

| Topic | Baseline in supplied snapshots | Action |
|---|---|---|
| IK envelope | `ik/1.1` | Reuse/validate unchanged |
| IK → Kristal build | `kristal.build.request/2.0.0` | Reuse unchanged |
| IK → Kristal ready | `kristal.artifact.ready/2.0.0` | Reuse unchanged |
| Kristal portable | `6.0.0`, `kristal_state/6.0` | Pin lock and test |
| IK v7 design pin | `7.0.0-draft.3.1` | Do not silently upgrade |
| Kristal v7 snapshot | `7.0.0-draft.3.2` | Resolve explicitly, likely updated IK lock after tests |
| Kristal v8–v10 | Additional layers/drafts | Out of v0 core scope unless authorized profile exists |
| Generic foreign integration | New capability | Draft separate IK profile/ADR |

## Handling incompatible versions

- **Reject** with machine-readable `UNSUPPORTED_CONTRACT_VERSION` and supported set (no private topology disclosure).
- Preserve original correlation/causation ID for permitted diagnostic telemetry.
- Do not mutate source data or send a partial semantic output.
- Attach digest and exact contract ID to alignment diagnostics.
- Warn on v7 draft pin skew in preflight, but do not rewrite current IK's v6 lock.
