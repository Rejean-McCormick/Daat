# 26 — Universal data onramp: product and architecture baseline

**Status:** `TARGET_DESIGN` / `USER_DECIDED` product direction; not an adopted IK external ingress profile, not operational readiness.  
**Date:** 2026-11-13. **Scope:** DaaT (`daat`) as the user-facing starting point for external data participation in kOA.  
**Precedence:** approved owner contracts/ADRs > approved DaaT ADRs > this target design > illustrative examples.  
**Reality check:** [19 — Implementation status](19-IMPLEMENTATION-STATUS.md) records the actual DaaT v0.3.0 offline library/CLI; do not infer deployed connectors or external admission from this document.

## 1. Product contract

A person or organization should be able to start with **"Bring my data into kOA"** without knowing the internal architecture. The source may be a PDF collection, Git repository, bibliographic corpus, accounting application, relational database, public dataset, stream, local archive or a collection of links. DaaT identifies an appropriate **integration journey**, not an invented universal ingestion semantics.

**'Everything starts at DaaT' describes the front door and contract boundary, not ownership of the whole workflow.** Existing owners execute acquisition, custody, semantic authoring, publication and operational effects. An expert should be able to add a source family by declaring a bounded adapter and approved mapping pack rather than modifying every kOA domain product.

### User-visible stages (target UX, not a claimed shipped UI)

1. **Describe or choose a source** — system, protocol, artifact type, account/tenant, purpose and rights.
2. **Inspect access** — capability, grants, retention, privacy and lawful/reusable scope; fail closed on missing authority.
3. **Preview** — source shape, estimated data volume, record families, change strategy, risks and sample provenance.
4. **Choose a route** — reference-only, bounded snapshot import or ongoing synchronization, subject to owner support.
5. **Prepare candidates** — delegate acquisition and custody; perform typed deterministic mapping and optional AI-assisted suggestions; show uncertainty and loss.
6. **Review** — obtain human/domain-owner decision for ambiguity, crosswalks and knowledge admission.
7. **Handoff** — invoke only the exact owner-approved interface; author/build/qualify/publish remain separate acts.
8. **Operate** — expose source revision, compatibility, checkpoint, denial, correction, revocation, status and recoverability without exposing private data.

The journey may legitimately end at a linked external reference or a rejected import. Success does **not** always mean creating a Kristal.

## 2. Non-negotiable ownership

| Concern | Responsible owner | DaaT role |
|---|---|---|
| Source system, operational records, credentials and exports | Source owner | Reference and check scope, never take implicit custody or mutate source |
| Research/crawling/authorized extraction | Skope / integrated EncyK or scoped source adapter | Select allowed route and validate exported boundaries; no competing crawler |
| Source/snapshot/representation custody | Médiathèque instance | Preserve and map verified, permission-filtered references; no duplicate media store |
| Identity, policy, scope and enforcement | Trusted host, Konfid, relevant receiver PEP | Fail-closed PEP with injected trusted decisions; not IdP/PDP |
| Transport, envelopes, profiles, routing, receipts | Interaction Kernel (IK) | Implement the boundary against **adopted** profiles, not invent wire profiles |
| External semantic crosswalk, lexical dictionaries and interpretation | Kristal Framework/diK, Kristalizer and domain reviewers | Preserve candidates, exact meanings and review states; no KQ/KP issuance |
| Structural design candidates | Arketype | Suggest candidate patterns, not prove identity/truth |
| Canonical Kristal state and local authoring | Framework + Kristal Authoring Kit | Prepare a reviewed input; never generate canonical state by its own authority |
| Build qualification, public release, activation | Separate qualified owner gates | Convey results; no publication or activation grant |
| Tasks/operational transitions | Orgo/receiving product | No side-effect orchestration or direct table writes |

**Important distinction:** the existing `kristal.build.request/2.0.0` IK profile is specific to its accepted senders and v6 path. It is **not** a generic external import profile. No such generic wire contract is approved by this document.

## 3. Three independent classifications

| Axis | Question | Examples | Owner/decision |
|---|---|---|---|
| **Transport/acquisition mechanism** | How are source bytes or references obtained? | user file, Git, read-only API, OAI-PMH, export, ODBC, SQL snapshot, stream, federated reference | Source adapter + receiving owner |
| **Source-content archetype** | What is contained? | bibliography, ledger, source code, legal corpus, temporal register, graph, telemetry, multimodal evidence | AI may propose; declared, reproducible review determines route |
| **Kristal structural archetype** | What organization might eventually be useful? | Arketype's 19 **design-only** templates, possibly several per source | Arketype suggestions; Framework/Kit authorized authoring |

This is a **many-to-many** relationship. A Git repository can contain documentation, proof artifacts, an academic corpus and executable source. An Acomba export may contain invoices, journal entries, cash payments and documents requiring distinct interpretation. Labels and external Q/P identifiers do not become KQ/KP by categorization.

## 4. Integration modes are orthogonal to mapping burden

- **Reference / federation:** reference remote owner-held data without mirroring; a live query is allowed only behind source-owned consent, policy and version controls.
- **Snapshot:** copy an authorized, bounded, versioned set of source evidence to a declared custody owner.
- **Incremental / synchronize:** obtain revisions or deltas with reliable checkpoints and source-side deletion semantics.

These are acquisition lifecycle modes, **not** replacements for the established DaaT mapping decision classes `aligned`, `adapted`, `incompatible`. Even aligned inputs still need authentication, authorization, schema validation, integrity and admission.

## 5. Processing boundaries

```text
Person/organization -> DaaT onboarding intent + source profile (target UX)
                  -> trusted host / source-owner authorization
                  -> approved source connector / Skope-EncyK (acquisition)
                  -> Médiathèque or approved source custodian (versioned references)
                  -> DaaT exact contract/policy checks + declared mapping
                  -> optional AI-assisted *candidates*, with evidence and review
                  -> Kristalizer / diK / Arketype design assistance (owner roles)
                  -> Kristal Authoring Kit + Framework authoring decision
                  -> independent qualification -> explicit release -> optional activation

IK owns all adopted cross-owner wire admission, delivery, events and receipts.
```

**The diagram is a target composition**, not a single presently adopted transport path. In particular no direct DaaT→Médiathèque, DaaT→Kit or AI→IK wire profile is asserted without an owner-approved schema.

## 6. What makes DaaT distinct from an ETL platform

Existing ETL systems solve extraction, transport, batch execution, schema evolution and change-data capture. DaaT should **borrow those capabilities selectively** (see [28 — Kintsugi](28-KINTSUGI-OSS-INTEGRATION.md)), while retaining its purpose: strict contract alignment, provenance-preserving admission, safety/authority checks and an explainable route toward Kristal-native authoring. DaaT is not a generic lakehouse, vector store, knowledge authority, data catalog of private content or workflow engine.

## 7. Functional acceptance (target)

- A contributor adds a new source **without** modifying IK, Kristal canonical schemas or Orgo; unsupported owner handoffs remain blocked.
- Every imported or federated datum keeps its source namespace, owner, revision/integrity and access scope; access may be revoked independently.
- AI suggestions remain proposals. Deterministic validation and owner review cannot be bypassed by high model confidence.
- On deny, unsupported version, cross-tenant context, lost required meaning, unavailable audit or uncertain side effect, the workflow stops or enters owner-controlled reconciliation.
- A second user can reproduce a frozen deterministic mapping from the same pinned inputs, profile, tool versions and policy-independent transformation configuration; nondeterministic AI results are separately identified as candidate evidence.
- No externally supplied data causes executable instructions to run or grants itself source access, canonical identities, authority or publication rights.

**Next:** [source taxonomy](27-SOURCE-TAXONOMY-AND-REGISTRY.md) → [Kintsugi lanes](28-KINTSUGI-OSS-INTEGRATION.md) → [journey and state machine](29-PROCESS-AND-HANDOFFS.md) → [Kristal interop](30-KRISTAL-STANDARDS-AND-PROVENANCE.md) → [testing](32-TEST-AND-THREAT-PLAN.md) → [implementation gates](33-CODING-ROADMAP.md).
