# Decisions pending owner approval — do not guess

These decisions are blocking only for affected milestones. An AI engineer should make a documented proposal and wait for owner approval when the decision changes a contract or safety boundary.

| ID | Decision | Safe temporary approach | Owner(s) |
|---|---|---|---|
| OD-01 | Is DaaT a new independent repo or a workspace/library inside IK? | Prepare docs-only repo; runtime must not duplicate IK | Product + IK |
| OD-02 | Runtime language/package strategy | Python library compatible with existing reference Python protocol, or documented alternative; no server by default | DaaT + IK |
| OD-03 | Approved generic external IK profile ID and version | Use existing `kristal.build.request/2.0.0` only for its existing scope | IK + receiver owners |
| OD-04 | Exact security trust provider / deployment model | Mock credentials **only** in tests; no public endpoint | Security + platform |
| OD-05 | Source/target contract pin release policy | Use exact checked-in owner locks; mismatch reported, not auto-repaired | Kristal + IK |
| OD-06 | IK v7 draft.3.1 vs Kristal draft.3.2 compatibility | Treat as explicit warning/block on new v7 features; leave portable v6 unchanged | Kristal + IK |
| OD-07 | Declarative mapping DSL semantics | Start with restricted operators and formal JSON Schema draft | DaaT + security |
| OD-08 | Publication/signing of alignment reports | Private unsigned local report, no public badge | Product + privacy |
| OD-09 | Scoring method public terminology | Publish raw per-scope burden/coverage/loss; avoid opaque ranking | Product + community |
| OD-10 | Journal retention and tenant partitioning | In-memory for library tests, no production service | Security + operators |
| OD-11 | Which real external system is first integration partner? | Synthetic example only | Product |
| OD-12 | Governance for accepting a loss-causing mapping | Default deny mandatory loss; require owner-approved exception | Domain owner + security |
| OD-13 | Repository and documentation license | Mark license undecided and do not assume GitHub default grant | Product/legal |
| OD-14 | Real Kristal-native connector API shape | Rely on current owner protocol and fake for tests; don't invent REST APIs | Kristal |
| OD-15 | Public SDK vs per-partner private adapter packs | Define neutral interfaces now, distribution model later | Product/security |

## Architecture decisions already taken in the conversation

1. DaaT **will remain** for external integration; it is not to be eliminated.
2. Small/large adapters are both legitimate.
3. Alignment reference should make voluntary convergence beneficial, without enforcement.
4. Native ecosystem must aim to avoid unnecessary internal semantic translation.
5. DaaT must not replace other components' responsibilities.

## Decision workflow

Write an ADR with context, options, selected recommendation, contract impact, backward compatibility, risks, test plan and responsible approver. No silent compatibility change is allowed based only on AI preference. See proposed [ADRs](decisions/).

## v0.3 owner security decisions awaiting approval

- Confirm actor service-principal representation and binding to Konfid and kOA policy (no guessed identity).
- Confirm DaaT policy ALLOW expiry support: local PEP requires `valid_until <= 120 seconds` and rejects missing expiry. Konfid response currently allows null.
- Confirm source ownership proof, referenced artifact byte/digest verification and approved locator resolution policy.
- Confirm host-owned authenticated Konfid RPC, kOA policy and kOA Audit Broker commit/receipt semantics.
- Confirm semantics and release scope of a **generic IK external ingress profile**; no wire handler shipped.
- Agree durable idempotency, outbox/reconciliation and error/blocked receipt policy before service deployment.
- Complete upstream license and dependency pin reviews before public publication.
