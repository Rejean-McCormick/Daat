# Vision, mission and invariants

## Core thesis

**Interoperability without uniformity. Convergence without coercion.** DaaT allows an external system to connect as-is, with whatever explicit transformations are needed. As the system voluntarily adopts shared contracts, the necessary **semantic adaptation** shrinks. Zero semantic transformations is a desirable possibility, **not a prerequisite to join**.

The common misunderstanding to avoid: **a large DaaT adapter is not a bad DaaT adapter**. It may be correct engineering for a well-functioning independent architecture. Smaller transformation distance means lower maintenance friction, not higher moral, educational or product quality.

## Actors and ecosystem goals

- **Native publisher/consumer:** follows the ecosystem's declared contracts without semantic adaptation.
- **Foreign publisher/consumer:** has an independent schema or meaning model; chooses an explicit DaaT adapter.
- **DaaT adapter author:** maps foreign semantics, documents ambiguities/losses and runs conformance tests.
- **Contract owner:** maintains versioned schemas, canonical identifiers and their interpretation.
- **Authority owner:** determines which identities are trusted and what operations are authorized.
- **Observer:** sees a reproducible integration report and can track alignment change over time.

## Non-negotiable invariants

| ID | Invariant | Failure example |
|---|---|---|
| INV-01 | `daat` is an external **boundary**, not a semantic source of truth. | Adapter invents a canonical Kristal identity from a label. |
| INV-02 | All transformations are explicit, versioned and attributable. | Hidden case-by-case renaming in business logic. |
| INV-03 | No transformation ever increases epistemic status by default. | Ingested unverified evidence becomes recognized knowledge. |
| INV-04 | Admission and authorization always occur where required; native-aligned does not mean trusted. | Aligned sender bypasses tenant policy. |
| INV-05 | Owner-preserving references survive the round trip. | DaaT claims to own a source-provided object. |
| INV-06 | Foreign identifiers remain foreign without an owner-sanctioned mapping. | Wikidata ID treated as Kristall KQ identity. |
| INV-07 | Version incompatibility fails closed. | v7 meta-artifact sent over a v6 build contract. |
| INV-08 | Missing fields and lossy transformations are visible, never silently erased. | Omitted qualifier silently changes interpretation. |
| INV-09 | Deterministic mapping for the same pinned inputs/profile. | Unpinned online lookup changes semantic output. |
| INV-10 | No second bus, source repository, workflow engine or access authority. | DaaT owns Orgo task state. |
| INV-11 | Alignment metrics are reproducible, transparent and nonpunitive. | Ranking applications by code line count alone. |
| INV-12 | Critical external operations are auditable and safely retryable. | Duplicate build produces untracked contradictory results. |
| INV-13 | Minimal DaaT is still a real integration boundary. | "Zero transform" skips security checks. |
| INV-14 | No external code executes merely because a mapping profile asks it to. | Mapping expression runs shell commands. |

## What DaaT deliberately does NOT do

Not a universal ontology, not a crawler, not a general ETL warehouse, not an application migration engine, not a centralized identity provider, not a curriculum evaluator, not an LLM-based semantic negotiator, not a generalized policy authority, not a scheduler, and not a replacement for IK or Kristal.

An AI may **suggest** possible mappings offline to the developer, but executable profiles must be reviewed, explicit and deterministic. An LLM must not decide authorization or silently synthesize semantic equivalences at runtime.

## What success looks like

1. A fully aligned external producer integrates through minimal DaaT with **zero semantic transforms** but all normal checks.
2. An intentionally heterogeneous system integrates using a documented mapping, preserving owner identity and epistemic qualifiers.
3. The author sees exactly which mismatch causes complexity and how an optional upstream schema change would reduce it.
4. Both exchange the **same contract-backed content**, verified by independent TCK fixtures.
5. The internal ecosystem remains free of mandatory DaaT translation steps.
