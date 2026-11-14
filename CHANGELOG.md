# Changelog

## 0.4.2 — kOA snapshot-based owner location and diK byte parity
- Resolve actual nested checkout paths from the explicit, bounded C0 `docs/inventory/repositories.json` inventory, never treating C0 as an owner authority.
- Add `kristal-owner-locations` CLI and `--inventory` to the existing owner preflight.
- Verify exact v11 schema byte parity of diK alpha.7 against Framework draft.4 as **read-only evidence**, without removing the functional-qualification blocker.
- Add negative fixtures for inventory attacks, duplicate entries, mismatched schemas, and false authority.
- Keep every existing security/IK/Kit owner boundary and canonical/write/publish prohibition.

## 0.4.1 — Offline Kristal review handoff (2026-11-13)

- Added strict read-only Kit/Framework pin preflight over explicit independent owner paths.
- Added evidence-bound, noncanonical local transfer packets for reviewed candidate subsets, with verification.
- No canonical authoring/import, IK ingress, live Konfid, source custody or publication is authorized.
- diK Framework draft.3 / Kit draft.4 interoperability remains unqualified and blocked.

# Changelog

## 0.3.0 — Owner-aligned security boundary

- Added independent verified actor requirement, typed policy request and bounded, intent-bound authorization responses.
- Added Konfid AccessRequest/AccessResponse port (requires trusted external transport).
- Added allowlisted offline external mapping entrypoint with authenticated provenance, tenant/capability checks and input size ceilings.
- Added security audit port and fail-closed integration into the existing v6 bridge, including replay re-authorization.
- Enforced Kristal output artifact ownership and tenant; denied unknown or restrictive policy obligations.
- Added negative security tests, original English documentation, AI instructions and threat/compatibility notes.
- No production IdP, real Konfid RPC, owner IK ingress profile, durable audit or journal, deployment, or release certification.


## 0.1.0-draft — 2026-10-12

- Created documentation-only DaaT repository specification.
- Preserved existing IK DaaT/Kristal reference boundary and portable v6 contract facts.
- Defined external interoperability + voluntary contract convergence model.
- Specified declarative mappings, alignment burden reporting, security, runtime lifecycle, TCK and AI implementation backlog.
- Documented real v7 draft pin discrepancy and decisions requiring owner approval.
- Added French product vision and proposed ADRs.

**No production DaaT service or code integration is shipped with this documentation release.**

## 0.2.0 — Offline library alpha

- Owner-contract validators and pin verification, strict mapping engine, alignment reports, IK v6 build port, test-only in-memory journal, CLI and security negative tests.
- Full owner integration is still blocked; see `docs/19-IMPLEMENTATION-STATUS.md`.

## Unreleased — 0.4.0 offline source-onramp prototype (2026-11-13)

- Added 36-family research catalogue, explicit eight access-lane metadata and strict read-only adapter manifests.
- Added noncanonical, bounded local PDF (optional pypdf), ZIP, Git, tabular, bibliography and Acomba-export readers.
- Added content-addressed evidence locations, user-asserted local rights, owner-review candidates and optional host-checked AI suggestions.
- Added fail-closed hosted connector SPI with injected verified principal/grant/output and Konfid-shaped policy/audit.
- Added local SQLite preview-only intent journal, private JSON preview output, verification and review packets.
- Preserved IK v6 restricted build semantics and existing DaaT mapping/security boundary; no generic network ingress, source-custody or v11 Kit APIs.
- Added offline tests and documentation of owner blockers; these additions do not make the project production-qualified.
