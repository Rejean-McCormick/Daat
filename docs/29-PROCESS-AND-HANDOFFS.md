# 29 — Universal onramp: journey, processing states and owner handoffs

**Status:** `TARGET_DESIGN` / **not a released API or production state machine**.  
**Read with:** [08 — Runtime](08-RUNTIME-AND-LIFECYCLE.md), [20 — Security boundary](20-SECURITY-BOUNDARY.md), [25 — Source custody](25-SOURCE-CUSTODY-BOUNDARY.md). Do not reinterpret existing IK profiles.

## 1. User journey vs bounded technical interactions

DaaT is the *entry experience* that diagnoses a source and coordinates **proposed** handoffs. This does not make DaaT the execution scheduler. When multiple tasks require execution or retries, invoke the **authorized owner mechanism**; do not implement an alternative IK queue or Orgo workflow. The below phases are useful to define interface behavior and acceptance tests, not proof of a persistent DaaT orchestrator.

| Phase | Required output/decision | System of record | Deny/stop condition |
|---|---|---|---|
| Discover | Typed source candidate, supported lane(s) | Source owner / trusted onboarding host | Unknown provider, unsafe file/URL |
| Authorize | Verified actor+workload, tenant, purpose, scopes and source-owner grant | IdP/Konfid/receiver PEP | Missing/expired grant, unsupported obligations |
| Plan | Exact source/target contracts, reviewable route, privacy/cost preview | DaaT reviewed mapping configuration | Ambiguous or lossy mandatory semantics |
| Acquire | Authorized source export with revision and integrity | Source owner/Skope/EncyK | ToS prohibition, corrupt bytes, unbounded source |
| Custody (if required) | Permissioned immutable source/snapshot/representation references | Selected Médiathèque instance or approved custodian | Missing custody receipt, cross-instance disclosure |
| Interpret | Noncanonical extraction/classification candidates | Source processing owner / authorized analyst | Hallucinated citations, ungrounded semantic matches |
| Map/admit | Reproducible declared transformation, no identity promotion | DaaT for its profile; IK for adopted transport | Schema/profile/policy failure, missing field, tenant mismatch |
| Review | Approved/rejected candidate crosswalk/knowledge proposal | Kristalizer/diK + authorized domain authority | Ambiguity or unapproved KQ/P equivalence |
| Author | Validated local Kristal workspace/artefact | Framework and Authoring Kit | Wrong draft/profile, unsupported migration |
| Qualify/release | Independent evidence and explicit destination authorization | Validation/release owners | No exact-binary qualification or owner release grant |
| Monitor/reconcile | Operational receipt and correction state | Each effect owner; DaaT only minimal correlation | Unknown side effect: hold and reconcile, never blind retry |

A source-specific route may omit many phases (e.g., reference-only). Not every imported source merits authoring.

## 2. Minimal integration metadata (conceptual, not a schema)

A trusted host may need the following **privacy-minimized, versioned records** to correlate a job:

- `integration_intent_ref`: host-local opaque identifier; **not** a new IK Profile ID.
- `source_owner_ref`, `source_system`, `source_record_id`, `source_revision` or immutable `snapshot_digest` when available.
- `requester_context_ref`: verified workload/actor, tenant and purpose **references**; never store raw credentials or assume fields are trusted because they were submitted.
- `source_rights_ref`, `classification`, `disclosure_policy` and revocation/expiry policy.
- `lane`, `adapter_id/version/digest`, `source_contract_ref/hash`, `mapping_profile_ref/hash`, `target_contract_ref/hash`.
- `extraction_manifest_ref` (if approved) and source-location evidence (file+page, database row+snapshot, repository commit+path).
- `candidate_refs`, reviewer/decision references and separated statuses of extraction, validation, recognition and publication.
- `owner_receipt_refs`, retry/idempotency context and recovery state.

All fields are descriptive. Their authoritative syntax belongs to the **owner's adopted** schema; until adoption, maintain them in documentation and offline fixtures only. Store only the minimum operational metadata required for a reliable integration and redact sensitive values from all logs.

## 3. Candidate and error state vocabulary (documentation-only)

```text
PROPOSED -> RIGHTS_PENDING -> PREVIEWED -> ROUTE_REVIEWED
         -> ACQUIRED/CUSTODIED (where applicable) -> CANDIDATES_READY
         -> MAPPING_REVIEWED -> OWNER_HANDOFF_PENDING
         -> OWNER_ACCEPTED / OWNER_REJECTED / RECONCILIATION_REQUIRED

Owner acceptance -> optional AUTHORING_REVIEW -> LOCAL_BUILD -> QUALIFICATION
              -> explicit PUBLICATION_AUTHORIZATION -> RELEASE/ACTIVATION
```

These are **illustrative workflow labels**, not DB tables, IK receipt codes, or status claims. The actual receiver and IK define their own state and terminal receipts. `OWNER_ACCEPTED != EFFECT_COMPLETED != KNOWLEDGE_VALIDATED != PUBLISHED`.

Errors should be expressed through the adopted owner/IK vocabulary, not new DaaT network error enums. At minimum, distinguish:

- `denied` (identity, rights, scope, tenant, policy)
- `unsupported` (provider, schema version, missing semantic capacity)
- `invalid` (malformed, tampered, conflicting revision, lost mandatory meaning)
- `temporarily_unavailable` (dependency/audit unavailable — fail closed)
- `effect_unknown` (write may have occurred — reconcile, do not retry blindly)
- `candidate_requires_review` (ambiguity, not a transport failure)

## 4. Deterministic core and bounded AI suggestions

**Deterministic pathway:** exact profile selection after approval, schema validation, normalization of declared units/timezones, fixed enrichment tables, identity namespace preservation, stable hashing and outputs, input/output invariant checks, and safe idempotency. For a fixed permitted source snapshot, profile, tool version and configuration, the transform must be reproducible.

**AI-assisted pathway:** document segmentation, schema hints, record taxonomy, entity mentions, candidate crosswalks, apparent duplicates, proposed Arketype combinations and anomaly explanations. The AI **never** determines user permissions, grants a source license, assigns canonical KQ/KP/KA/KS, silently resolves conflicting metadata or authorizes publication. Record model/version/settings and relevant source citations under approved data retention rules. A nondeterministic candidate output cannot be sold as deterministic canonical derivation.

**Review:** accept/reject/correct candidate, with exact source positions and justified decision. Semantic decisions are represented under Framework/Kristalizer/diK/Kit owners, not in a new DaaT knowledge ledger.

## 5. Bulk and incremental semantics

- A run identifies a stable source snapshot, revision or bounded interval; cursor movement alone is not a proof that target effects happened.
- Pagination, shards and retry checkpoints are source-adapter responsibility; the same logical chunk maps consistently to a pinned transform.
- Upserts and deletions require a **declared** policy; neither erases history, source custody or previously recognized Kristals automatically.
- When source and destination differ in transactional semantics, use an **owner-approved** outbox/reconciliation path with terminal receipts.
- When an external source revokes access, stop further acquisition and follow the receiver's retention/deletion policy; do not assume that all already published derived knowledge must disappear automatically.
- Maintain bounding quotas and capacity planning outside the pure DaaT mapping DSL.

## 6. Zero-transform route

If a source already speaks an approved native contract, DaaT may use a minimal adapter and emit a zero semantic transformation report. **This still requires all applicable identity, policy, admission, digest, profile and audit checks.** A source claiming to be "native" is not trusted without proof.

## 7. Blocked contract decisions

No public upload endpoint, no general HTTP ingestion listener, no generic IK profile, no Médiathèque source-ref wire profile, no universal Kit import and no source-account connector credential vault are approved by this target description. Their **schema IDs, owners, migrations, authorization and bilateral test evidence are TBD**. Refer to [33 — Roadmap](33-CODING-ROADMAP.md) for gates.
