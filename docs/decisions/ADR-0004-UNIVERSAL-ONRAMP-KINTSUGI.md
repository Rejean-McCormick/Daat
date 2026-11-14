# ADR-0004 — Universal external-data onramp with Kintsugi adapters

**Status:** `PROPOSED` — DaaT design decision for owner review, **not an adopted IK or Kristal owner ADR**.  
**Date:** 2026-11-13. **Related:** [ADR-0001](ADR-0001-DAAT-PURPOSE.md), [architecture](../03-ARCHITECTURE.md), [26](../26-UNIVERSAL-DATA-ONRAMP.md), [33](../33-CODING-ROADMAP.md).

## Context

People possess data in incompatible systems: files, software repositories, bibliographic databases, accounting/ERP, public datasets and event streams. DaaT already provides a scoped offline mapping/security boundary; kOA owners already define acquisition, custody, semantic authoring and publication. Building a new monolithic ETL/knowledge warehouse would duplicate those authorities.

## Proposed decision

- Present DaaT as the universal **entry and mapping/admission boundary**, while delegating actual source acquisition and custody to appropriate owner-authorized components.
- Describe integrations with three separate axes: transport lane, source content type, possible Arketype design composition.
- Reuse open-source connectors/parsers under Kintsugi `Mimic`, `Annex` or `Reference-only` after exact license/security review; maintain Kompendio-style provenance/credits and isolated contracts.
- Preserve native IK/Kristal provenance, artifact references, identities, validations and release boundaries. Do **not** add a universal provenance canon or treat RO-Crate as mandatory.
- Start PDF/Git prototypes; treat PhilPapers and Acomba as explicitly rights-scoped pilots. Block unapproved generic IK source ingress and v11 Kit handoff.

## Alternatives

1. Build an all-in-one DaaT crawler, data warehouse and semantic engine — **rejected**: duplicate authority and operational debt.
2. Put every source directly into the Kristal Kit — **rejected**: bypasses source rights, mapping/admission and evidence custody.
3. Embed a single existing ETL platform wholesale — **deferred**: license, security, operational and mapping fit uncertain.
4. DaaT only as v6 narrow build translator — **retained as existing capability**, insufficient as target user onramp alone.

## Compatibility and rollout

Additive documentation only for now. Existing `kristal.build.request/2.0.0`, IK wire profiles, DaaT 0.3.0 draft mapping format, Kristal canonical schemas and provider records remain unchanged. Future proposals require **independent owner ADRs**; do not apply hypothetical schema IDs as though accepted.

## Risks and mitigation

Source rights/ToS (gate each import), secrets/PII (tenant isolation, minimize and redact), AI semantic hallucination (candidates + review), duplicate knowledge identity (Framework authority), sidecar supply chain (pins/SBOM/credits), incompatible owner revisions (fail closed and publish contract diff), retry after partial effect (durable reconciliation).

## Adoption and verification gates

This ADR can be accepted **inside DaaT** only after the DaaT owner reviews scope, risk and workload. It does **not** override IK, Médiathèque, Framework, diK, Kit, Konfid or source-owner contracts. Any capability claiming external transport, source custody, semantic state or publication requires those separate owners' explicit revisions and bilateral TCK results.
