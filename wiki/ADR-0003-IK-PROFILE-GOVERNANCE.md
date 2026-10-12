# ADR-0003 — Preserve owner contracts; version generic external profiles

**Status:** Proposed for review · **Date:** 2026-10-12

## Decision proposed

Keep IK `kristal.build.request/2.0.0` and `kristal.artifact.ready/2.0.0` as the existing **portable Kristal v6** interaction surface. Do not widen their semantics. New external capabilities (e.g. non-Kristal `inventory.read`) require separately named, owner-approved IK profiles with explicit security, authority, output and receipt obligations.

## Compatibility note

The IK snapshot's v7 pin is draft.3.1; Kristal Framework reports draft.3.2. Those must be reconciled through explicit contract owner tests and pin releases, not silent downgrades/upgrades. Portable v6 remains unchanged.

## Dependency

Approval by Interaction Kernel and any receiving domain owner before implementation of live generic external IK exchange.
