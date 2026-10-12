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
