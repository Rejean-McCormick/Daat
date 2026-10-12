# ADR-0001 — DaaT as external boundary and alignment reference

**Status:** Proposed for owner review · **Date:** 2026-10-12

## Context

The native ecosystem aims to share canonical versioned contracts, making internal semantic conversions unnecessary where possible. Independent external apps have legitimate different architectures and must still be able to participate. Existing IK ADR-IK-07 already defines DaaT's Kristal-facing anti-corruption boundary; generalized external access is a new proposed capability.

## Decision proposed

Maintain DaaT as an external admission/compatibility boundary. Permit minimal adapters for native-shaped partners and extensive adapters for independent systems. Publish a reproducible, scoped alignment analysis where transformation burden is visible but does not prevent conformance. DaaT shall not own semantic or operational authority and shall reuse IK delivery/contracts where applicable.

## Consequences

- No mandatory internal DaaT semantic conversion for aligned native systems.
- External system integration can be incremental and voluntary.
- New non-Kristal IK Profile(s) require IK owner ADR and versioned contracts.
- DaaT runtime remains narrow; larger semantics reside in explicit app-specific mapping packs.
- Alignment numbers are not product-quality rankings.

## Rejected alternatives

1. **Eliminate DaaT entirely:** removes the external anti-corruption edge and the optional developer pathway.
2. **Mandate fully native internals for every external app:** excludes legitimate heterogeneity.
3. **Centralize all business meaning and state in DaaT:** duplicates Kristal/Orgo/other owners.
4. **Treat adapter source-code size as compliance score:** easily gamed and semantically misleading.

## Status caveat

This is a proposed product ADR; it does not supersede accepted `Interaction-Kernel/docs/adrs/ADR-IK-07` until reviewed and any contract changes are approved by owners.
