# Specification precedence and document status

**Release:** `0.1.0-draft` (2026-10-12)  
**Nature:** Build-oriented Markdown documentation only.

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
- Exact DaaT mapping schema not yet implemented or owner approved.

Do not select versions or authorities by guesswork.
