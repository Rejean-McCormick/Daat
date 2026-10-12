# Architecture and authority placement

## Target logical picture (PROPOSAL)

```text
                         SHARED CONTRACTS & TCK
                     (owned by IK/Kristal/other domains)
                                |            ^
       +------------------------+------------+--------------------+
       |                        |                                 |
  External App A          External App B                       Native Apps
  (native-shaped)         (foreign-shaped)                  (Orgo/Ekole/etc.)
       |                        |                                 |
 Minimal DaaT profile    DaaT mapping pack                         |
       |                        |                                 |
       +------ DaaT boundary --+                                 |
                      |                                           |
         authenticate / validate / authorize                       |
         transform ONLY if needed / measure                        |
                      |                                           |
                      +---------- Interaction Kernel -------------+
                                      |
                            owner-native interfaces
                               Kristal / Orgo / ...
```

**Existing factual scope:** IK documents DaaT as its boundary **in front of Kristal/Kristall**. Generalized foreign-to-ecosystem participation is a new architectural direction; implement only via compatible versioned extension profiles, not by widening the old `kristal.build.request/2.0.0` semantics.

## Logical components (not necessarily separate services)

| Component | Owns | May not own |
|---|---|---|
| Adapter/profile registry | Metadata and pinned references to reviewed mapping packs | Source of truth for foreign data |
| Contract resolver | Integrity-verified refs to upstream versions | Forks of canonical contracts |
| Admission facade | Authenticating via configured trust providers, authorization decision based on receiver rules | Global IAM/IdP |
| Mapping engine | Pure transformation under reviewed profile | Semantic recognition/authority |
| Alignment evaluator | Contract diffs, transform inventory, loss inventory, conformance results | Application quality ratings |
| Connector port | Calls owner-native interface with minimum permissions | Owner's operational tables |
| Receipt emitter | IK-compatible receipts/events | Another message bus |
| Optional delivery journal | Local correlation/idempotency/retry/recovery metadata | Long-term document/media storage |
| Diagnostics | Privacy-safe trace and metrics | User content surveillance |

## Ports-and-adapters shape

```text
                 +---------------------------+
    IK Envelope ->| Admission port            |
                 | Verify profile + authority |
                 +-------------+-------------+
                               |
                               v
                  ContractPin + MappingProfile
                               |
                      deterministic mapping
                               |
                               v
                  NativeConnectorPort.invoke()
                               |
                        owner interface
                               |
                               v
                 Output contract validation
                               |
                               v
                   IK Receipt + ArtifactRef
```

Suggested interfaces, *not already present as shipped code*:

```python
class MappingProfile(Protocol):
    id: str
    version: str
    def transform(self, source: Mapping, context: Mapping) -> Mapping: ...

class ContractResolver(Protocol):
    def verify_pins(self, contract_set: str, digests: Mapping) -> None: ...

class AdmissionPort(Protocol):
    def authenticate_and_authorize(self, interaction: Mapping) -> Mapping: ...

class NativeConnectorPort(Protocol):
    def invoke(self, operation: str, validated_input: Mapping) -> Mapping: ...
```

Do not replace the upstream `execute_build(envelope, manifest, mapping, kristal)` signature merely to look like these examples. Build a compatibility wrapper or propose an IK PR if necessary.

## Three integration modes

**Mode A — Aligned:** sender payload already matches required domain-native schema. No meaning conversion. Perform authn/authz/admission/schema checks; transport reference; return receipts.

**Mode B — Adapted:** source has a different shape or vocabulary. Apply a reviewed and pinned profile, with field-by-field provenance, loss disclosures and tests.

**Mode C — Incompatible:** mandatory semantics are absent, authority cannot be proven, or unsafe loss is unavoidable. Reject (or quarantine for developer review, **not** silently deliver); return actionable error.

## Ownership and tenancy

- Tenant isolation exists at source, receiver and DaaT journal if any. No cross-tenant profile lookup by default.
- Provenance and source owner are immutable along the conversion chain.
- DaaT does not generate business state transitions in Orgo or grade pupils in Ekole.
- Read-only contract caches are versioned by digest and treated as untrusted until verified.
- Generic DaaT accepts external systems through IK; the downstream owner's own access check is still mandatory. Trust is not transitive.

## Deployment strategy

Default to **library + CLI + IK adapter**. Add a long-running ingress service only if the current IK delivery architecture requires one; its transport shape, authentication mechanism and hosting topology require a separate ADR. Never create a public unauthenticated endpoint simply because a demo needs a URL.

## Authority table

| Decision | Owner |
|---|---|
| Is this participant authenticated? | Identity/trust provider + receiver verification |
| Can this operation run for this tenant? | Receiver authorization policy |
| Which IK profile is permitted? | IK and relevant profile owner |
| Which schema defines a `kristal_state`? | Kristal |
| Are two external IDs semantically equivalent? | Domain authority/Kristal mapping process |
| Is a workflow task complete? | Orgo |
| Is a learning objective mastered? | Ekole + authorized validation rules |
| Which declared conversion runs? | Reviewed DaaT mapping profile |
| What is the visible adaptation burden? | DaaT alignment evaluator under documented method |
