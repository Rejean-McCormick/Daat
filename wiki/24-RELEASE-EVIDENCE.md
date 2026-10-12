# DaaT v0.3.0 — Reproducible release evidence

**Date:** 2026-10-12. **Scope:** local synthetic/offline library, not production-certified.

| Check | Local result |
|---|---|
| `PYTHONPATH=src:tests python -m pytest -q` | **99 tests passed** (23 bridge, 5 CLI, 14 contracts, 19 mapping, 38 security) |
| `python -m compileall -q src tests examples` | Passed |
| `PYTHONPATH=src python -m daat verify-contracts` | Verified 9 IK owner files; portable Kristal 6.0.0 |
| `PYTHONPATH=src python -m daat validate-build examples/ik-build-envelope.json` | Passed (owner IK profile) |
| `PYTHONPATH=src python -m daat alignment-report mappings/native/profile.json` | Golden verified; burden 0 |
| `PYTHONPATH=src python -m daat alignment-report mappings/foreign-inventory/profile.json` | Golden verified; burden 4 |
| `PYTHONPATH=src python examples/fake_host_demo.py` | Generated owner-schema-valid synthetic accepted/final/event records using fakes |
| `python -m pip wheel . --no-deps --no-build-isolation` | Built `daat_boundary-0.3.0-py3-none-any.whl` |
| clean pip `--target` install of wheel, run `python -m daat verify-contracts` from `/tmp` | Passed; bundled schemas resolved outside checkout |
| `python tools/check_markdown_links.py` | See command output |
| `python tools/verify_manifest.py` | See command output |

## Boundaries of this evidence

Unit and synthetic tests are **not** external actor JWT verification, real Konfid/kOA authorization, production audit, HTTP security, IK routing, true Kristal semantic compilation, real student consent/privacy verification, signed attestations or durable exactly-once processing.

The release's `REPOSITORY-MANIFEST.json` hashes **local source files only**. It is neither an independent signature nor a supply-chain attestation. License policy unresolved; redistribution of owner contract copies requires rights confirmation.

## Next owner integration tests

1. Konfid/kOA real ALLOW with `valid_until` and supported obligations, plus timeout/deny/outage.
2. IK and Kristal owner profiles, actual receiver action and final owner-side artifact verification.
3. Restart/crash durability and secure audit broker / reconciliation.
4. External workload and actor cryptographic binding including cross-tenant attack simulation.
5. Independent KonnaxionDiag/LevelUpDiag release gates with signed artifacts if approved.
