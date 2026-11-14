# 31 — Four pilot playbooks and reusable connector patterns

**Status:** `TARGET_DESIGN`, **not connector releases**. Each pilot must first prove *permissioned access + source/custody integrity + declared mapping + negative tests* with the actual owners. Start local and read-only; no generic internet crawler, live ERP write or semantic auto-publication.

## Pilot 1 — Local PDF collection (P0)

**Goal:** user-selected document set → verifiable source/evidence references → noncanonical knowledge candidates. **Lane:** L1 (bounded local artifacts); optional L4 for large authorized archives.

**Source inputs:** PDF/PDF-A, authorized scanned images and ZIP manifest; explicit selected root; ownership/use authorization; classification. **Potential OSS:** Docling Annex, optional Tika for detection. Treat language models, OCR weights and dependency assets as separately licensed/versioned.

**Steps:**

1. Preflight extensions, magic bytes, archive member count/depth, decompression ratio, MIME, malware policy and tenant grants; never execute embedded scripts/macros.
2. Preserve unmodified original and digest at designated custodian; record file path as a scoped source-local reference rather than a public storage URL.
3. Extract page text, table cells, structure and possibly OCR; preserve `(snapshot_ref, page, section/region, extraction_version)` for every citation.
4. Separate direct text, extraction uncertainty, human annotation and AI-inferred candidate assertion; no inferred fact inherits the document's authority.
5. Validate exact schema and reviewed DaaT mapping; submit candidates to authorized Kristalizer/Kit boundary only if adopted.
6. Compare reruns: identical deterministic extraction settings should yield stable anchored sections. Nondeterministic OCR/AI outputs are versioned candidates, not reproducible canonical claims.

**Must reject:** corrupt/encrypted-without-key, huge recursion/zip bomb, wrong tenant, invalid user grant, unavailable audit, external URL inside PDF interpreted as a command, missing source location or fabricated citation.

**Acceptance fixture:** 2-page PDF with table and false friend entity name; versioned output evidence mapping for pages/regions; intentionally malicious archive and duplicate filename; no Kristal publication side effect.

## Pilot 2 — Git repository / GitHub (P0)

**Goal:** immutable code/documentation snapshot → candidate knowledge about a project and its evidence. **Lane:** L5, optionally L2 for issues/PR metadata when licensed and scoped.

**Source inputs:** explicit repository and pinned commit SHA, permitted branch/tag as a selector only, path allowlist, scope and license; authorizing principal. Never execute project content or install its packages as an extraction prerequisite.

**Steps:**

1. Check repo visibility, selected revision, grant and project license/redistribution rights; exclude `.git` credentials, secrets, generated vendor folders and oversized files.
2. Preserve commit SHA + path + blob SHA and a read-only source snapshot; identify Git LFS/submodule boundaries separately rather than silently following them.
3. Parse safe text/metadata; recognize that a README states an *author's claim*, while tests establish only their observed environment.
4. Classify source content into potential code, documentation, spec, proof and timeline archetypes (not one fixed ARK from the fact it is Git).
5. Map with pinned fixture and reject unresolved version or license conditions.
6. Future delta mode compares commit trees but never treats force-push/deletion as permission to rewrite a canonical Kristal.

**Must reject:** unpinned moving-ref ingestion, untrusted submodule traversal, malicious repository instructions, repo token logging, copied secrets, unlicensed vendored binary.

**Acceptance fixture:** repo with two commits, renamed file, conflicting assertion in README vs code test, one secret fixture; demonstrate anchored references and zero code execution.

## Pilot 3 — Bibliographic corpus (P1)

**Goal:** authorized scholarly metadata → provenance-rich bibliographic candidates and optionally referenced full text, subject to rights. **Lanes:** L2/L3 and possibly L4.

**Examples:** Crossref, OpenAlex, PhilArchive, PhilPapers **within their separately verified permitted interfaces**. A public search page or JSON response does *not* imply permission to harvest substantially, retain or redistribute the underlying corpus.

**Steps:**

1. Check per-provider terms, API limits, metadata/full-text licensing, use case and right to republish; if an interface disallows bulk copying, stop or use reference-only mode.
2. Preserve source record ID, DOI/ORCID (when valid), retrieval timestamp, permitted revision, license, work type and attribution.
3. Deduplicate as **candidates**; author homonyms, withdrawn articles, preprints and published versions are not silently collapsed.
4. Propose potential Arketype structures (collection, semantic reference, research memory), optionally using ML classification only as review assistance.
5. Submit reviewed source-level records to the appropriate semantic owner. Citations document evidence and publication metadata, not automatic acceptance of every claim in a paper.

**Must reject:** absent lawful interface, unauthorized PhilPapers bulk replication, unsupported full-text rights, mixing external taxonomy IDs with KQ/KP, DOI collision and incorrect publication status.

**Acceptance fixture:** five synthetic records with same title/different DOI, withdrawn version and ambiguous author; deterministic dedupe report with no semantic identity auto-merge.

## Pilot 4 — Acomba accounting exports (P1; private-host only)

**Goal:** owner-authorized **read-only** accounting data → typed snapshots/relationships/evidence without creating a new accounting system. **Lane:** L6 or L1 for officially exported files.

**Source inputs:** actual edition's approved SDK/ODBC/export mechanism, customer-granted service account and minimum table scopes. Availability of a connector and exact schema must be verified on a sandbox installation; do not invent a universal Acomba API.

**Steps:**

1. Confirm tenant-owned source, purpose, location of private data and retention; never connect production accounting data to a public test service.
2. Export a transaction-consistent snapshot where feasible; preserve per-system customer/supplier/invoice/payment/entry IDs, period, currency, debit/credit semantics and source revision.
3. Define separate source-content patterns for economic event, supporting document, accounting entry, payment, balance and reporting snapshot. They are **not** interchangeable.
4. Use only explicit unit/currency/date/tax transforms; AI may propose column correspondences but does not post entries, prove invoice payment or decide tax treatments.
5. Send only permitted references/aggregations to reviewed mapping/authoring; source ledger remains sole operational authority.
6. Add incremental sync **only after** change-marker validity, delete/correction handling and exact replay tests are established.

**Must reject:** missing owner rights, multi-tenant confusion, unresolved amounts/currency sign, inconsistent snapshot, changed ledger with reused checkpoint, any write attempt.

**Acceptance fixture:** wholly synthetic ledger with two currencies, voided invoice, partial payment, duplicate document ID and period correction; reports must preserve economic/accounting distinctions.

## Common pilot evidence checklist

| Check | Required |
|---|---|
| Owner/source access proof | Named principal, tenant, purpose, exact scope and expiry/grant lifecycle |
| Revisions + immutable bytes | Source revision/snapshot, file/record digest, source-location anchors |
| Source legality | Code/content/license/ToS assessment and allowed redistribution/retention |
| Security | No secrets in logs, bounded resource consumption, deny-by-default PEP, source-read-only behavior |
| Determinism | Golden + invalid fixture, profile hashes, reproducible non-AI transform; AI candidate trace separated |
| Semantic protection | No auto KQ/P/KA/KS issue; no recognition or actionability upgrade |
| Cross-owner integration | Exact adopted interface and owner-approved bilateral fixture, or recorded BLOCKED |
| Operations | Replay, recovery, revocation, correction/deletion and `effect_unknown` reconciliation |

Do not call the pilot `integrated` on unit tests or a fake SDK. See [32](32-TEST-AND-THREAT-PLAN.md) and [33](33-CODING-ROADMAP.md).
