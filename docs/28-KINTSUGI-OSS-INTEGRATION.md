# 28 — Kintsugi/Kompendio approach for DaaT open-source integration

**Status:** `TARGET_DESIGN`; component choices are **candidates**, not pinned or legally approved dependencies.  
**Purpose:** reuse mature extraction tools while preventing a second data platform, second authority, license contamination or opaque transformations.

## 1. Mimic, Annex or Reference

| Strategy | Meaning | Appropriate if | Required credit |
|---|---|---|---|
| **Mimic** | Independently implement a general design pattern, not copied protected code or data | Existing engine would dominate kOA, violate deployment policy or be unmaintainable | Cite project and idea in architecture/Kompendio references; do not misrepresent authorship |
| **Annex** | Run or link an open-source component as an isolated, replaceable tool behind an explicit adapter | Small bounded responsibility, compatible license/dependencies and auditable outputs | Preserve upstream copyright/license and notices as the applicable license requires; publish dependency inventory/SBOM |
| **Reference-only** | Link to a tool or data source without embedding its code, data or state | No redistribution rights, reference catalogue use, optional external user choice | Cite canonical URL, rights and limitations |

A SaaS provider or proprietary SDK may be an approved **external adapter** without being open source. Never call such code OSS, and never equate a metadata/API permission with bulk download or republication rights.

Kintsugi is a curated toolchain pattern; **Kompendio is the reference and credits catalogue**. It does not become DaaT's mapping or legal authority.

## 2. Shortlisted capabilities and boundaries

| Need | Candidate project(s) | Architecture posture | Why this is not a core dependency yet |
|---|---|---|---|
| PDF structure, tables, OCR-assisted parsing | Docling | Optional Annex as controlled document-processing worker | Validate models, assets, subprocess isolation, accuracy and distribution rights |
| Broad file type detection/metadata | Apache Tika | Optional Annex if Docling alone insufficient | JVM operational footprint, parser attack surface and overlap |
| Replicable source extractors | Meltano Singer SDK/taps | Mimic connector contract; selective Annex to an audited tap | Each tap independently maintained/licensed; no blanket trust |
| Incremental bulk loader | dlt | Optional Annex only where scaling requires it | Prevent creation of DaaT-owned data warehouse |
| Exact review/reconciliation UX | OpenRefine | Mimic interaction principles; optional isolated Annex | Candidate matches are never canonical KQ equivalence |
| Database change streams | Debezium | Later conditional Annex in source-owned environment | Requires source DB authority, safe CDC configuration and retention |
| Flow orchestration | Apache NiFi / Apache Hop | Learn from replay/observability patterns; not default Annex | DaaT must not duplicate IK/Orgo orchestration |
| Broad commercial/open connector marketplace | Airbyte ecosystem | Reference/evaluate individual connectors | Product/code licenses and connector terms vary; no bulk inclusion assumption |
| Virtualized RDF views | Ontop | Study for federation pattern | External semantic projection is not Kristal identity or canonical proof |

No version number, license classification or production safety attestation is asserted for an *unselected* candidate. Before selecting one, verify the **exact tag, SPDX identifier, transitive dependency licenses, model weights, dataset rights, container/image layers and deployment mode**, including cloud/service limitations. See [release controls](33-CODING-ROADMAP.md).

## 3. Annex isolation contract (proposed, subject to owners)

An Annex worker MUST:

1. Receive a **bounded, permissioned job** from a trusted host; its job object is not an IK wire profile until IK has adopted it.
2. Have no ability to mutate Kristal canonical state, grant an actor privileges, publish content, or write source system records.
3. Operate with minimal read-only scopes, tenant separation, declared egress and sandboxing; no ambient secrets or unrestricted URLs.
4. Return content-independent **artifacts or source-owned references** and extraction metadata, including version/hash/config, source page/row/commit position, warnings and omitted fields.
5. Be deterministic where its operation is deterministic; mark nondeterministic output and keep AI/model prompts, versions and confidence as **candidate provenance** with applicable privacy controls.
6. Preserve originals with their custodian and respect deletion/revocation; no unapproved second data store.
7. Fail explicitly on unsupported encoding, corrupt data, ambiguous input, unavailable policy/audit or excessive resource use.
8. Run exact-version functional, negative, tenant-isolation and performance tests before being enabled for a source family.

For proprietary connectors, use the same contract plus license terms and no unauthorized code redistribution.

## 4. Credits and legal compliance files (for *selected* components)

For each approved Annex include **one maintained entry** in a third-party ledger, e.g. an eventual `docs/third-party/` registry (not created as fake approved credits in this pack):

```text
Project: <upstream canonical name and URL>
Purpose in DaaT: <bounded capability>
Mode: Annex | Mimic | Reference
Version/tag and digest: <verified immutable ref>
License(s): <verified SPDX id(s), plus full applicable text/notice locations>
Copyright holders: <as required by actual notices>
Source availability/offer: <if applicable>
Modified: yes/no; modifications/diff and attribution obligations
Transitive dependencies/models/assets: <manifest + license review>
Data terms: <separate from code license; approved uses/restrictions>
Security/deployment review: <date, owner, findings and status>
```

Publish any license texts, copyright/NOTICE statements, change notices and source offers when the **specific applicable licenses** require them. Attribution alone does **not** authorize copying, bulk indexing, redistribution, web scraping or use of models with separate terms. SPDX/CycloneDX SBOMs can be generated for traceability; they are evidence tools, **not** legal clearance certificates. Obtain legal/product approval for any GPL/AGPL/ELv2/noncommercial/source-available condition relevant to the proposed deployment. Never assume an `Annex` process magically avoids copyleft or other license conditions.

## 5. Kintsugi selection scorecard (each criterion recorded, not collapsed)

- Source/target semantic fidelity and location-specific evidence preservation.
- Exact owner authority and privacy posture, including offline/on-prem viability.
- License and data terms, model weights, third-party notices, update policy.
- Reliability, deterministic replay, corruption handling and no unbounded storage.
- Scope of privileges, vulnerability/advisory response and sandbox feasibility.
- Operational footprint (CPU, RAM, GPU, JVM, container), performance and auditability.
- Replacement cost and vendor lock-in; can the same contract be fulfilled by another worker?

A tool is admitted only for a named workload, version and host posture; no global blanket "approved" badge.

## 6. Interface version policy

The sidecar's release is pinned independently from the DaaT adapter and independently from the owner source/target schemas. Replacement, upgrade or model change requires fixture comparison, semantic-difference report and reauthorization when behavior/rights change. A parser's fact-extraction confidence never substitutes for domain review.

**Related:** [source taxonomy](27-SOURCE-TAXONOMY-AND-REGISTRY.md), [pilots](31-PILOT-PLAYBOOKS.md), [test plan](32-TEST-AND-THREAT-PLAN.md).
