# Conformance and verification (TCK)

## Scope and principles

Tests must distinguish **correct schema shape**, **correct authorization**, **correct semantic preservation** and **correct integration behavior**. A document, mock or golden fixture alone is not proof of a deployed service.

## Four conformance tracks

**C1 Contract conformance:** verifies source and target schemas, exact version/digest pin, IK profile and semver compatibility.  
**C2 Semantic preservation:** verifies identity namespaces, provenance, epistemic qualifiers, optional/required semantics, transformation inventory and loss policy.  
**C3 Security and runtime:** verifies authentication/authorization, artifact refs, malicious locators, idempotency, retries, observability and tenant isolation.  
**C4 Integration:** verifies handoff through the real IK adaptor/client and owner-native implementation, end-to-end correlation with receipts/events. Must not be passed by mock-only tests.

## Gate table

| Gate | Positive test | Mandatory negative test |
|---|---|---|
| IK schema | Valid complete `ik/1.1` envelope | Missing `source` or malformed `profile` |
| IK profile | Approved `kristal.build.request/2.0.0` | Wrong target / unsupported version |
| Contract lock | Verified Kristal portable `6.0.0` lock | Modified digest / v7 meta-field in v6 wire |
| Authentication | Correct sender credentials and audience | Forged sender / expired credentials |
| Authorization | Allowed tenant, capability, artifact scope | Cross-tenant / missing mandate |
| Mapping | Golden input equals expected native | Missing field or loss forbidden |
| Provenance | Source owner and evidence preserved | Adapter claiming canonical ownership |
| Epistemic semantics | Uncertainty and applicability maintained | Unverified source promoted to recognized |
| Identity | External ID remains external | External ID relabeled Kristall KQ |
| Replay | Same digest idempotent | Same key, different digest rejected |
| Artifact | Correct verified `ArtifactRef` | Tampered digest or unsafe locator |
| Receipt | Acceptance + final with correlation | Missing final or false success after failure |
| Metrics | Reproducible transform inventory | Burden zero despite hidden conversion |
| Offline | Contract checks with pinned local files | Network unavailable causes silent schema fallback |

## Test layout after implementation

```text
tests/
  unit/{test_pin,test_mapping,test_metrics,test_identity}.py
  security/{test_authority,test_tenant,test_ssrf,test_injection}.py
  contract/{test_ik_envelope,test_ik_receipt,test_kristal_state}.py
  integration/{test_ik_adaptor,test_kristal_native_fake,test_native_owner}.py
  fixtures/
    aligned-native/
    foreign-inventory/
    epistemic-negative/
    version-skew/
    malicious-locator/
```

Use exact owner schema and validator with format checking; tests in this proposed layout are **not shipped yet**.

## Minimal v0 test vectors (specification)

1. **Native A:** one supported operation, identity mapping rules only; target schema validates; `burden_points=0`; admission/authorization still tested.
2. **Foreign B:** source field aliases plus one structural conversion; transform report lists each rule; target artifact matches golden fixture.
3. **C with lost qualifier:** a required qualifier cannot be represented; rejects with `MAPPING_LOSS_FORBIDDEN`.
4. **Version skew:** IK's v7 draft.3.1 design pin differs from the Kristal repo's draft.3.2; preflight displays discrepancy without upgrading silently.
5. **IK build:** existing `execute_build` function checks `daat` target, v6, profile and mapping ID; integration wrapper enforces additional real admission gates.
6. **Duplicate:** same `(key,digest)` does not cause a second side effect; different digest rejected.
7. **Out-of-order result:** event correlation works even if observer receives later record first.
8. **Integrity:** tampered ArtifactRef digest blocks publication.
9. **External account without trust:** even 0-burden mapping rejects.
10. **Output labels:** `working` must never become `reference` merely by mapping.

## Release gates

- `docs_only`: schema/docs links valid; source traceability complete; no runtime claims.
- `library_alpha`: C1/C2 unit+golden fixtures pass; no prod auth or service claim.
- `integration_alpha`: C1–C3, fake owner and IK adapter tests pass, failure semantics documented.
- `integration_beta`: C1–C4 against real pinned owner implementations in isolated test environment, no sensitive data.
- `production_candidate`: independent security review, operator runbook, recovery/rollback drills, profiling, monitoring and sign-off from each contract owner.

## Build/CI commands (planned, NOT asserted to exist)

```bash
python -m pytest tests/unit tests/contract tests/security
python -m pytest tests/integration
python -m daat.cli verify-contracts --lock path/to/approved.lock.json
python -m daat.cli validate-mapping mappings/example/.../profile.json
python -m daat.cli alignment-report --profile mappings/example/.../profile.json
```

Implementers must update this section to reflect actual CLI once built; do not falsely claim these commands already run.
