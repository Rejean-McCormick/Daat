# DaaT and the Skope → Médiathèque custody boundary

**Status:** `TARGET_DESIGN` / offline integration instructions; **no adopted DaaT↔Médiathèque profile**. This page does not add a new IK envelope, network listener, persistent source catalog or semantic identity authority.

## Current source-backed relationship

1. **Skope / integrated EncyK 0.14.0** is the acquisition producer. It exports `encyk.source-evidence-handoff/2.0.0` with references, source/evidence checksums and noncanonical external identity hints.
2. **Médiathèque engine 0.5.1** receives this package only into a deliberately selected local library instance. On success it assigns durable source/snapshot/representation references and emits a consumer-specific, **unsigned** `koa.encyk-source-handoff-receipt/1.0.0` receipt.
3. **DaaT 0.3.0** is a separate, offline **external mapping and security boundary**. It cannot treat a handoff manifest or acceptance receipt as a verified permission to read source bytes, change the Médiathèque catalog, or author canonical KQ/KP/KA/KS identities.
4. **Kristal Kit / semantic authoring** must independently approve any mapping/crosswalk that could change a workspace. Wikidata Q/P are external identifiers, not Framework KQ/KP identities.

## Design for a future source-reference admission (not implemented)

| Component | Owner decision required | Must reject |
|---|---|---|
| Médiathèque instance | Which source/snapshot/representation references may be disclosed, to which tenant/principal and for what purpose | Absent custody receipt, missing stored bytes, unknown visibility/license, wrong instance, unapproved metadata |
| Trusted calling host | Authenticated transport identity and actor, proof of source reference permission, access decision transport and audit persistence | Caller-supplied identity fields as trust, stale/expired decision, mismatched source revision |
| DaaT | An **owner-approved**, versioned mapping profile and allowlist for a *specific* use case, not arbitrary generic JSON | Unknown profile, undeclared fields, raw file fetch, untrusted ownership or absent PEP dependencies |
| Authoring Kit | Explicit review/approval of mapping proposal and exact Framework schema profile | Automatic semantic identity minting, import without consent, unsupported Draft.3/Draft.4 compatibility |

**No new contract ID is asserted here.** The exact version, field schema, disclosure policy, owner approvers and producer/consumer fixtures remain open for the relevant repositories. The existing `kristal.build.request/2.0.0` profile **must not be repurposed** as a generic Médiathèque source import request.

## Tests to preserve

- Deny a consumer of a raw Médiathèque receipt when no approved source-reference mapping profile exists; do not infer authorization from a receipt's `status: accepted`.
- Deny any mapping when the host source verifier rejects a source reference, even if schema and tenant seem valid.
- Pin and test valid/invalid mapping schema, actor and tenant, missing or expired Konfid policy and missing audit sink before any future actual adapter.
- When owners adopt the future source-ref schema, add **bilateral fixture tests** against the real Médiathèque library/source API and real Kit import; synthetic DaaT tests do not prove production integration.

## Implementation handoff

**Branch 01 → Branch 02:** approved source references, provenance and explicit owner disclosure permissions must be supplied to Kit reviewers. **Branch 01 → Branch 08:** the trusted caller, Konfid decision binding and receiver-side PEP must be agreed without making DaaT an authentication service. Keep the current DaaT package 0.3.0 offline and fail closed until those dependencies are supplied.
