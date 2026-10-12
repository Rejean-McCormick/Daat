# DaaT v0.3.0 — Security-optimized offline release validation

## Scope and status

This document reports tests performed on a local offline Python implementation on 2026-10-12. It is **not** a security certification, IK live integration, or production approval. The 0.2.0 report is superseded.

## Executable functionality

- `src/daat/security.py`: scoped PDP/PEP port, exact intent binding, decision TTL, supported obligations, fail-closed audit.
- `src/daat/konfid_port.py`: host-injected translator to the actual owner-shaped Konfid AccessRequest/AccessResponse. No live Konfid transport.
- `src/daat/external.py`: offline authenticated, allowlisted mapping boundary. No external IK wire endpoint.
- `src/daat/bridge.py`: pinned IK v6 build with required actor, policy and audit and native output ownership/tenant checks. In-doubt memory journal only.
- Previously implemented contract and mapping validator, alignment evaluator and local CLI are preserved.

## Commands used

```bash
PYTHONPATH=src:tests python -m pytest -q
python -m compileall -q src tests examples
PYTHONPATH=src python -m daat verify-contracts
PYTHONPATH=src python -m daat validate-build examples/ik-build-envelope.json
PYTHONPATH=src python examples/fake_host_demo.py
python tools/check_markdown_links.py
python tools/verify_manifest.py
python -m pip wheel . --no-deps --no-build-isolation
```


**Results:** 99 tests passing; native alignment burden 0, foreign inventory burden 4; 9 pinned IK files verified; bundled wheel verified from a clean target installation; source links and integrity manifest verified.

Validation details and artifact checks are included in `docs/24-RELEASE-EVIDENCE.md`.

## Not delivered

Real JWT / OIDC / actor assertion verification; live Konfid/kOA services and audit broker; signed policy response; native Kristal compile; generic IK external ingress profile; durable idempotency, outbox and security telemetry; production reverse proxy; student data authorization; public compliance credential.

Source licensing and redistribution of pinned upstream schema snapshots require explicit rights review before open-source publication.
