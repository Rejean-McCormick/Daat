# Specification precedence and document status

**Release:** `0.1.0-draft` (2026-10-12)  
**Nature:** Original design baseline. **Code has since been added in v0.2.0; see [implementation status](19-IMPLEMENTATION-STATUS.md).**

## Normative precedence

1. Actual accepted owner contracts and ADRs in the upstream project (IK, Kristal, relevant receiver).
2. Subsequently accepted DaaT ADRs if compatible with upstream owners.
3. DaaT source baseline and invariants.
4. Proposed DaaT specifications and planned behavior.
5. Examples, diagrams and illustrations.

Statements tagged `PROPOSAL` are targets, not claims of implemented code. The word **MUST** in a proposal means 'must hold if implementing that proposal', not that upstream has already adopted it.

## Blocking compatibility questions

- Existing IK v7 design pin draft.3.1 vs Kristal snapshot draft.3.2.
- Generic non-Kristal capability requires new owner-reviewed IK Profile.
- Authentication/trust and runtime/deployment model not selected.
- Local DaaT mapping draft is implemented but not an IK-owner-approved wire profile.

Do not select versions or authorities by guesswork.

<!-- daat-universal-onramp-docs-2026-11-13 -->
## Onramp documentation baseline — 2026-11-13

Documents [26–34](26-UNIVERSAL-DATA-ONRAMP.md) and proposed [ADR-0004](decisions/ADR-0004-UNIVERSAL-ONRAMP-KINTSUGI.md) express an expanded, implementation-ready **target design**. They neither change the approved owner precedence above nor the actual offline v0.3.0 implementation described in [19](19-IMPLEMENTATION-STATUS.md). The old v0.1 release label on this page is a historical specification baseline, **not** the currently implemented package version.
