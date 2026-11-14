# 27 — Source taxonomy, integration lanes and adapter catalogue

**Status:** `TARGET_DESIGN`; catalog entries are research candidates, not supported connectors.  
**Companion inventory:** [36 source families](data/source-family-landscape-36.csv) (research-derived, French labels, advisory priorities).  
**Binding contract:** DaaT mapping profiles remain governed by [06 — Mapping profiles](06-MAPPING-PROFILES.md); this catalogue does not define a new IK profile.

## 1. Eight reusable access lanes

| Lane | Input reality | Representative protocols | Source-owner proof needed | Typical retention |
|---|---|---|---|---|
| **L1: Local artifacts** | Uploaded files/directories/archive | PDF, DOCX, CSV, JSON, ZIP, TAR, image | Explicit user/tenant rights to read and copy | Versioned custodian snapshot; no raw bytes in DaaT journal |
| **L2: Read API** | SaaS/business application | REST, GraphQL, SOAP, OData | Scoped token, API terms, principal and requested fields | Opaque owner-held cursor + digest |
| **L3: Harvest/export** | Bibliographic or cultural portal | OAI-PMH, SRU, feeds, DCAT, IIIF | Interface terms, harvest authorization and licenses | Provider stable IDs + revision/resumption token |
| **L4: Bulk snapshot** | Large open/enterprise dataset | JSONL, Parquet, RDF, SQL export, WARC, PBF | Distribution rights, scope and checksum provenance | Partition and snapshot manifest |
| **L5: Versioned tree/object** | Code and object repositories | Git, versioned S3 objects, Drive revisions | Repo/ref ACL, specific commit/object version | Commit/blob or object version and hash |
| **L6: Enterprise DB** | Transactional ERP/CRM/ledger | ODBC, SDK, read-only SQL, approved CDC | DB grants, consistency isolation, encryption, tenant | Source transaction snapshot/high-water mark |
| **L7: Event stream** | Event/message producer | Webhook, MQTT, CloudEvents, Kafka, OPC UA | Source-authenticated channel and approved event semantics | Bounded ordered watermark and dedupe scope |
| **L8: Federated reference** | Source remains in place | URI, signed manifest, source-specific query | Authorized link, revocation behavior and remote policy | Typed source reference; no assumed perpetual availability |

**Security design:** adapters run outside the declarative mapping expression interpreter. Execution of user-supplied code, arbitrary credentials, internet fetching and unrestricted source URLs are never permitted just because a lane exists. A host must independently enforce allowlists, egress policy, time/size limits and delegated credentials.

## 2. The catalogue has four orthogonal descriptors

1. **Source family**: bibliographic index, ERP, Git, repository, document archive, graph, time series, etc.
2. **Acquisition lane(s)**: L1–L8; multiple lanes may be valid for one provider.
3. **Source-content shape(s)**: text corpus, ledger events, entities/relations, scientific observations, media evidence, software snapshots, etc.
4. **Potential Arketype composition**: zero/many candidate ARK templates; it is a recommendation for later authoring, not a direct conversion.

The [CSV](data/source-family-landscape-36.csv) enumerates **36 families** with example sources, formats, paths, synchronization mode, candidate Arketype IDs and risks. It is a **research input**: no entry establishes legal rights or verified integration readiness. Source-family IDs in the CSV are local catalogue row numbers, **not** semantic KQ/KP identifiers.

## 3. Adapter record (conceptual metadata, not a wire schema)

Each provider adapter should declare and receive review for:

| Field group | Required information |
|---|---|
| Identity | adapter ID + version + code digest; maintainer; owner and license assessment |
| Capabilities | lane, source family, supported protocol/version, read/write boundary, sync mode |
| Trust | actor/tenant binding method; scopes; network/equipment boundary; disclosure policy |
| Data | record kinds, size/volume guardrails, encoding and schema provenance, deletion semantics |
| Integrity | stable source ID, snapshot/revision, checksums, source-side consistency guarantee |
| Mapping | exact source contract + owner-pinned target contract, versioned DaaT mapping reference, fixtures |
| Output | source-owner ExportManifest / ArtifactRef or an explicitly approved equivalent; no invented generic IK envelope |
| Operations | idempotency scope, timeouts, resumption checkpoint, retry limits, revocation and purge route |
| Legal | license, attribution, terms/ToS, privacy, storage locality and redistribution status |
| Assurance | fixture suite, malicious-input tests, supported deployment, maintenance maturity |

The adapter registry is **configuration metadata only**. DaaT must not become the canonical storage for source data, secrets, or semantic IDs. Any runtime registry implementation requires an explicit ADR, retention policy and review.

## 4. Selection and fallback algorithm (deterministic decision policy)

- Reject if identity, grant, purpose, license/ToS or source contract cannot be established; do not use a model to waive rights.
- Detect supported lane(s) from declared provider capabilities and verified object type; use AI only as assistance for ambiguous types.
- Rank eligible lanes by least privilege, provenance fidelity, source load, repeatability, full/partial data requirement, auditability and operational cost. Record reason codes.
- If a safe federated reference is sufficient, prefer not to copy confidential or restricted original content.
- Where snapshot is required, route to source-owning acquisition/custody controls before DaaT mapping. No untrusted raw bytes become authoritative by entering a library.
- Mapping profile is chosen only after comparing exact source/target semantics; aligned, adapted and incompatible are independent of lane selection.
- If the selected lane cannot preserve mandatory fields, authorization, revision or audit, return **unsupported/blocked** rather than a lossy pseudo-success.

## 5. Scale characteristics

**Small:** a single consented PDF or repository; user-facing preview may be interactive.  
**Medium:** a departmental document corpus or periodic accounting export; partition and batch with safe resume.  
**Large:** bibliographic bulk dump, data lake or graph dump; source-owned immutable manifests, bounded shards and streaming through specialized engines are preferable.  
**Continuous:** enterprise CDC or telemetry; add only after snapshot and replay contracts have passed bilateral owner tests.

An adapter must declare limits on bytes, record count, nested archive depth, query cost, API rate, timeout and memory. A batch watermark/checkpoint is **operational metadata** only and may not be treated as source truth or an IK transport receipt.

## 6. Definition of done for a new adapter

An adapter is listed as `proposed`, `fixture-tested`, `owner-approved`, `bilaterally-tested` or `operationally-qualified`. These are documentary status labels and do not change domain authority. Minimum release evidence: source + target contract hashes, golden and malicious fixtures, nondisclosure checks, license notices, source permission proof, cancellation/revocation behavior, recovery/replay tests and exact peer-owner acceptance.

## 7. Do not conflate source classification with Kristal design

Arketype's 19 design archetypes are declared in its own `arketype/archetypes/` files and `arketype/docs/14_FRAMEWORK_V11_ET_DIK.md`. Their labels are **not** a canonical graph; the Framework and Kit own KQ/KP/KA/KS integrity. DaaT may expose candidate ARK IDs as a review suggestion; it may neither mint KQ/P nor assert a completed v11 authoring state.

**Related:** [31 — Pilot playbooks](31-PILOT-PLAYBOOKS.md) and [32 — Test and threat plan](32-TEST-AND-THREAT-PLAN.md).
