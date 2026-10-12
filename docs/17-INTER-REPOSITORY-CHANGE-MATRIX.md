# Inter-repository change matrix: what an AI must edit, and where

Goal: preserve domain ownership instead of putting everything in the new DaaT repo.

| Repository | Existing source baseline | Proposed changes | Explicit non-change |
|---|---|---|---|
| **DaaT (this repo)** | Offline library and injected security gates | Mapping profile DSL, measurement, CLI, test harness, boundary library/adapter glue, optional runtime journal | No duplicate IK transport or Kristal semantics |
| **Interaction-Kernel** | `adapters/daat/`, `contracts/profiles/kristal/...`, IK envelope/receipt owner code | Add approved generic external profiles if necessary; update IK adapter integration; contract lock and tests | Do not relabel `kristal.build.request/2.0.0` as generic; do not silently change `ik/1.1` semantics |
| **Kristal-Framework** | Portable v6, additive v7 and later layers, `DaaT-Boundary.md` | Publish/test owner-approved native connector capabilities; align pin matrix; document explicit new meta-artifact profiles when needed | Do not let DaaT mint semantic IDs or define evidence recognition |
| **kOA_Digital_Ecosystem** | Knowledge boundary documentation and repo inventory | Update architecture inventory and integration diagrams to reflect generic external DaaT capability after acceptance | Do not imply current generic gateway already deployed |
| **Orgo** | IK and Kristal integration adapters | Implement consumer support only for specifically approved profile/event; add end-to-end tests | Do not use DaaT to complete Orgo tasks by side effect |
| **Ekole** | Pedagogical knowledge/exercises and evidence | If an actual capability needs exchange, expose owner-defined evidence/artifact contract and tests | DaaT never grades or stores permanent student histories |
| **Kontexte** | Scenario catalog and render/runtime demo | Define only authentic integration artifacts/events for a real use case; supply sanitised fixtures | DaaT never executes its mission logic |
| **SemantiK** | Linguistic realization services/contracts | Only if external app requests an approved language capability; contract-owned integration | DaaT does not invent translated meaning |
| **External partner** | Independent source schema/operational state | Own connector/export, mapping approvals, immutable evidence and credentials | No forced database rewrite to match ecosystem internals |

## PR routing rules

- New/changed **IK envelope, profile, receipt** → IK PR + relevant owner review.
- New/changed **Kristal schema, semantics, portable lock** → Kristal PR + compatibility review.
- New mapping from **foreign source A** → DaaT mapping pack PR plus source-owner fixture approval.
- New claim of **semantic identity or recognition** → domain/Kristal authority; cannot be solved in DaaT.
- New **Orgo task status** → Orgo owner; cannot be created by DaaT mapping.
- DaaT alignment **scoring convention** → DaaT ADR + public method version bump.

## Version coordination workflow

1. Freeze all contract owner revisions and digests.
2. Create cross-repo compatibility matrix and baseline fixture results.
3. Propose owner-owned contract changes in owner repos before dependent implementation.
4. Build new DaaT mapping pack against accepted versions only.
5. Run owner TCK and DaaT C1–C4 gates.
6. Publish exact supported version matrix; document unsupported branches.
7. Keep old fixtures to prevent unintentional behavior drift.

## Example: when an external application sends a ticket-complete event

- Foreign app publishes immutable event with source identity.
- DaaT validates sender and maps under an approved specific profile.
- IK transports to the recipient.
- Orgo verifies its own authority and decides task transition.
- Receipt/evidence references return along the accepted contract.

If no approved Orgo/IK event profile exists, **do not fake one**. Write the required IK/Orgo ADR and test fixtures instead.

## Security owner integration assignments (v0.3)

- **Konfid**: Validate request/response field shape, service and actor authentication, downstream kOA policy expiry, obligation vocabulary, reason codes, real policy transport. DaaT only implements local PEP contract conformance.
- **kOA**: Publish policy decision validity and authoritative Audit Broker contract; security governance owner, not DaaT.
- **Kontainer**: Owner integration option for secured Kristal artifact packaging; DaaT cannot reinterpret cryptographic promises.
- **KonnaxionDiag / LevelUpDiag-Orgo**: Independent diagnostic and release gates; tests must not self-issue certification.
- **Interaction Kernel**: External ingress profile, delivery receipts, correlation, rejection behavior and eventually generalized transport admission.
- **DaaT**: Enforce the bound policy result, mapping allowlist, operator/resource limits and scoped audit record. No service credentials to all systems.
