# DaaT — External Interoperability & Alignment Boundary

**Code version:** `0.3.0` (offline library/CLI security-boundary alpha). **Runtime status:** pre-production, **not a deployed IK service**.

> DaaT makes integration possible without imposing uniformity. An external application's necessary semantic adaptations can be recorded and measured as a transparent, reducible *alignment burden*, not a judgment of the application's quality.

DaaT is an **external-facing integration boundary**. A natively aligned client may need no semantic mapping; other clients use explicit, tested, version-pinned mapping profiles. Every client still needs authenticated admission, owner authorization, schema validation, and safe artifact access. DaaT never replaces IK, Orgo, Kristal, or an owner's identity or storage authority.

## Security boundary — optimized v0.3.0

The **semantic mapping burden may approach zero; the security obligations never do**. This release adds an explicit policy enforcement point (PEP) integrated with the existing owner-shaped Konfid `AccessRequest` and `AccessResponse` through **trusted host-injected interfaces**.

- `daat.security.SecurityGate`: deny-by-default authorization, exact intent digest binding, max 120-second validity, enforce supported obligations, mandatory minimal audit sink.
- `daat.konfid_port.KonfidPolicyPort`: formats the current Konfid access contract; **caller supplies authenticated TLS/workload-bound RPC**. This is not an HTTP client, identity provider or live Konfid integration.
- `daat.external.ExternalMappingBoundary`: in-process **external mapping API**, requiring a verified workload + actor, owner input verification, mapping profile allowlist, bounded JSON and Konfid-backed policy. It is **not** an IK wire message format or listener.
- `daat.bridge.V6BuildBridge`: all build paths now require host-verified actor, scoped policy permission and audit, including cached replay. Native output owner and tenant are checked.

This is an intentional **API tightening**: callers that used the 0.2.0 fake build bridge without policy and audit injections will now fail closed. See [Security integration](docs/20-SECURITY-BOUNDARY.md), [Konfid compatibility](docs/21-KONFID-CONTRACT-ALIGNMENT.md), and [Threat model](docs/23-THREAT-AND-TRUST-MATRIX.md).

## Delivered features

- Python package and `daat` CLI (offline, no listener, no network access).
- Strict IK `ik/1.1` **owner-schema validation**, pinned vendored copies and SHA-256 baseline verification.
- Portable Kristal **v6 `6.0.0` lock verification** and explicit v7 draft discrepancy warning (not an upgrade).
- **Local draft** declarative mapping format with allowlisted operators; no dynamic scripts, model calls, external schema fetching or silent field loss.
- Native identity mapping and a foreign inventory alias/enum example, each with golden fixtures.
- Reproducible per-capability alignment reports: support/coverage, transformation burden, explicit exclusions; **not** a software ranking or conformance certificate.
- IK-compatible `MappingProfile.map_export` wrapper.
- Dependency-injected `kristal.build.request/2.0.0` build bridge that enforces owner IK schemas and requires **host-provided identity, actor verification, policy, audit, integrity and native Kristal implementations**. Tests use clearly labeled fakes. It generates schema-checked receipt/event *records* but does not send them via IK.
- Memory-only idempotency guard: replay of a completed request is safe in one process; uncertain native effects deliberately block re-execution pending owner reconciliation.
- Contract, mapping, security, CLI and fake-bridge tests; GitHub Actions workflow.

**Not delivered:** production authentication, signed policy proof verification, real Konfid/kOA transport, durable audit broker, artifact retrieval, live IK transport, real Kristal compilation, generic external IK profiles, durable journal, deployed HTTP gateway, signed public reports, v7/v10 support. These are blocked on upstream owner decisions, not hidden under mocks.

## Quick start

```bash
python -m venv .venv
# Linux / macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e '.[dev]'
daat --help
```

Run these exact commands inside the repo:

```bash
daat verify-contracts
daat validate-mapping mappings/native/profile.json
daat validate-mapping mappings/foreign-inventory/profile.json
daat map mappings/foreign-inventory/profile.json mappings/foreign-inventory/examples/golden.input.json
daat alignment-report mappings/native/profile.json --out out/native-report.json
daat alignment-report mappings/foreign-inventory/profile.json --out out/foreign-report.json
daat validate-build examples/ik-build-envelope.json
python -m pytest -q
```

Expected mapping example:

```json
{"external_id":"outside:product-123","quantity":15,"unit":"centimeter","owner":"external-merchant"}
```

Two mapping examples are deliberately different: native burden `0`; foreign inventory burden `4` (two aliases, one enumerated value mapping). Neither indicates a system is better or worse. These measure **only the stated capability scope and fixture**, and real integrations must independently disclose upstream transformations.

## Project layout

```text
src/daat/            library, CLI, IK schema checks, mapping, alignment, build port
contracts/owners/ik/ read-only owner schemas, exact snapshot digests and Kristal v6 lock
contracts/daat/      local draft mapping schema, NOT a released IK profile
mappings/            pinned native and external examples with golden fixtures
examples/            complete test IK command/manifest (synthetic; no trust evidence)
tests/               unit, security and fake-native integration tests
docs/                detailed specifications and source provenance
wiki/                English GitHub Wiki export mirror
```

## Integration in code (host-owned authentication required)

```python
from pathlib import Path
from daat.bridge import V6BuildBridge

# The host supplies real IK-admitted identity/actor verification, Konfid/kOA-backed policy,
# audit persistence, artifact proof, and the real Kristal native client.
# Deliberately fails closed if these are not supplied:
bridge = V6BuildBridge()  # fails closed: no host identity/policy/audit/verifier injection
# bridge.process(ik_envelope, export_manifest, Path("mappings/native/profile.json"), native_client)
```

For the separate **Skope/EncyK → Médiathèque source-custody lane**, see [source custody boundary and remaining owner gates](docs/25-SOURCE-CUSTODY-BOUNDARY.md). A storage receipt is not a DaaT mapping profile or Kristal approval.

See [Implementation status](docs/19-IMPLEMENTATION-STATUS.md), [AGENTS.md](AGENTS.md), [full specifications](docs/README.md) and [AI backlog](docs/15-AI-BUILD-BACKLOG.md).

## Important upstream contract boundaries

The provided IK baseline restricts `kristal.build.request/2.0.0` to approved sources and `daat` as target. It is **not** a universal external IK transport profile. DaaT will not overload that existing build contract with unrelated external commands. Kristal semantic identity/recognition remains owned by Kristal. Orgo continues to own its workflows, and IK owns delivery.

## Security and publication

This is an offline prototype suitable for synthetic fixtures, **not real personal or student data**. There is no production trust provider or owner-side approval. Vendored upstream schema copies are integrity-pinned for local conformance only; before making the repository public, confirm redistribution rights and [select explicit licenses](LICENSE-POLICY.md). No license is granted by the present documentation policy.

## Synthetic end-to-end library example

After installing the project, run `python examples/fake_host_demo.py`. This verifies that the in-process build flow constructs IK-schema-valid records. Its `DemoOnly*` providers explicitly **do not authenticate real systems or verify real artifact bytes**. Never expose this example through an HTTP server.

## Verifiable source integrity

Run `python tools/verify_manifest.py` to verify the tracked ZIP source contents against `REPOSITORY-MANIFEST.json` and `python tools/check_markdown_links.py` for local documentation links. The manifest is a local checksum inventory, **not a signed attestation**.
