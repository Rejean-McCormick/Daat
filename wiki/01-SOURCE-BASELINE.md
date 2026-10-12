# Source baseline, provenance and status

**Snapshot inspected:** user-supplied `snaps.zip` (15 projects, inspected 2026-10-12). This document distinguishes source-supported facts from DaaT repository design choices.

## Verified in provided repositories — not claims of a production service

| Area | Source path | What it establishes |
|---|---|---|
| IK adapter | `Interaction-Kernel/interaction_kernel/adapters/daat/README.md` | DaaT `daat`, narrow anti-corruption/admission boundary; no source acquisition or semantic authority. |
| IK code | `.../adapters/daat/build_mapping.py` | `execute_build(...)` reference helper checks the `kristal.build.request/2.0.0` profile, `target.system=daat`, mapping ID and v6 contract set before mapping and invoking a client. It does **not** prove authentication, durable service or full artifact validation. |
| IK lock | `.../adapters/daat/kristal_lock.py`, `kristal.lock.json` | A v6 portable consumer lock checker with known expected digests. |
| Accepted decision | `.../docs/adrs/ADR-IK-07-daat-kristal-v7-boundary.md` | Stable naming; v6 build contract stays portable v6; v7 meta-artifacts need new explicit profiles. |
| Transport contracts | `.../contracts/schemas/envelope.schema.json`, `artifact-ref.schema.json`, `receipt.schema.json`, `export-manifest.schema.json` | IK `ik/1.1` envelope/receipt/ArtifactRef/ExportManifest shapes. |
| IK build profile | `.../contracts/profiles/kristal/kristal.build.request/2.0.0/{profile,payload.schema}.json` | Target DaaT, authority required, durable/idempotent, mapping profile and v6 `6.0.0` contract fields. |
| IK result profile | `.../contracts/profiles/kristal/kristal.artifact.ready/2.0.0/{profile,payload.schema}.json` | Artifact references required, event from `daat`, stages including `kristal-state`, `working`, `reference`, etc. |
| IK authority | `.../docs/security-authority.md` | Sender claims are not receiver authorization; fail closed on incompatible, unknown or unauthorized input. |
| Kristal boundary | `Kristal-Framework/spec/v7/DaaT-Boundary.md` | Optional boundary in front of Kristal; Kristal is not dependent on DaaT; v6 portable state remains unchanged. |
| Kristal status | `Kristal-Framework/spec/v7/00-overview/specification-status.md` | Kristal v7 `7.0.0-draft.3.2` in this snapshot. |
| IK design pin | `Interaction-Kernel/interaction_kernel/docs/kristal-daat.md` | IK describes v7 design baseline `7.0.0-draft.3.1` separately from v6 lock. **Version skew is real and needs a decision/test.** |
| Ecosystem description | `kOA_Digital_Ecosystem/docs/1-Overview/Components-Kristal-and-Daat.md` | Acquisition handoff → DaaT → Kristal-native v6; other products keep their own authority. |
| Ecosystem technical reference | `kOA_Digital_Ecosystem/docs/2-Technical-Reference/20-nodes/daat-kristal-bridge.md` | Provenance/epistemic labels, source status, recognition and Reader Policy must not be conflated. |
| Orgo integration | `Orgo/apps/api/src/orgo/integrations/interaction-kernel/` and `.../kristal/` | Existing integration surfaces to analyze for integration tests; **not** a DaaT execution implementation. |

## Owner decisions made in this design discussion

1. Internal ecosystem should pursue direct **native contract alignment** rather than an omnipresent mapper.
2. DaaT **must exist as an external integration boundary**, including for natively aligned external systems.
3. A foreign application may implement a small or substantial DaaT adapter; substantial integration is legitimate and is not a quality defect.
4. The adapter burden is a **signal of distance from native contracts**, not a simplistic score based on line count or a mandatory product ranking.
5. Publish a reproducible reference and conformance tests to encourage voluntary alignment.

These are **proposed requirements for this new repo**, not statements that IK/Kristal already support a universal external DaaT gateway.

## Versioning clarification

- Existing **portable build surface:** Kristal `6.0.0`, `kristal_state/6.0`, IK profile `kristal.build.request/2.0.0`.
- Existing **IK design pin:** Kristal v7 draft.3.1.
- **Kristal-Framework snapshot** shows v7 draft.3.2; v8–v10 are additional design layers, with v10 draft.3.1 documented.
- This package does **not** select a new canonical runtime release or change existing locks. A dedicated compatibility ADR/test gate is required.
- Exact digests stay in the upstream lock file; don't duplicate magic hashes in new prose or change them to match a test.

## Evidence labels

- `SOURCE`: text or code found in supplied snapshot.
- `DECISION`: architecture direction specified by product owner.
- `PROPOSAL`: implementation details to be approved/tested.
- `UNVERIFIED`: not proven by provided code or tests.

Never promote `PROPOSAL` to `SOURCE` in status reports.
