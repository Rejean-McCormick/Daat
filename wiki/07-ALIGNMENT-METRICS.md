# Measuring alignment distance without penalizing diversity

## Philosophy

The **amount of necessary adaptation** can be a useful proxy for contract alignment. It is **not** a universal measure of software quality, sophistication, correctness, cultural suitability, business value or compliance. A larger adapter is legitimate. This metric offers a **voluntary improvement reference**, not a forced uniformity test.

A count of source code lines is particularly weak: complex conversion may be hidden upstream; correct code may be verbose; some native security checks never disappear.

## Measurement unit

Measure each **contract edge**: `(source profile/version/digest, destination profile/version/digest, capability, scope, mapping version)`.

Do not aggregate unrelated capabilities without naming scope and weights. Two apps can have equal scores while supporting different capabilities; reports must display coverage alongside distance.

## Observable record per field/rule

- source path and contract meaning;
- destination path and contract meaning;
- class of transformation (identity/alias/structural/value/contextual/lossy/unsupported);
- invertible? precision? required-field preservation? provenance preserved?;
- declared external context and manual review reference;
- verified by a matching golden fixture?;
- supporting test IDs and version pins.

## Core measures (PROPOSAL)

Let:

- `N` = number of evaluated target semantic obligations in the declared capability scope (not number of all fields in entire ecosystem).
- `S` = number of those obligations verified as supported.
- `B` = sum of transformation burden weights over all verified mapping rules, using 0/1/2/4/8 per class in `06-MAPPING-PROFILES.md`.
- `L` = number of explicitly permitted lossy operations (with independent explanation).
- `U` = number of unsupported **mandatory** obligations.
- `X` = number of owner/semantic ambiguities unresolved.

Calculate:

```text
coverage = S / N               # only if N > 0
burden_points = B              # not normalized by code size
burden_per_obligation = B / N
loss_count = L
unsupported_mandatory = U
ambiguous_count = X
zero_semantic_transform = (B == 0 and L == 0 and U == 0 and X == 0)
```

**These are the canonical raw metrics.** No single opaque score is normative. If a visual gauge is desired, it MUST state the method, denominator, tested capability scope, rounding, version, and whether unsupported fields are included; it must never suggest a universal quality ranking.

A report is `conformant_for_scope = true` only if supported/required obligations and all owner-prescribed TCK/security gates pass. Conformance is independent of `B`: a well-mapped foreign system can conform with `B > 0`.

## Guard against gaming

1. Compare actual source/output semantics with pinned contracts; do not count transformations only in `mappings/`. Hidden conversions performed inside the external app before the boundary must be declared **if they exist solely to satisfy the target contract**.
2. Use golden external fixtures from the application's normal native output, not a specially hand-cleaned export.
3. Include extra data loss and all assumptions; rejecting an unsafe integration is not marked 'worse quality'.
4. Keep separate security/admission overhead; zero semantic mapping does not yield a zero integration runtime.
5. A declared unsupported capability is not hidden by dropping it from metrics after the fact; publish `scope` transparently.
6. Run independent third-party fixtures when certification/qualification matters.
7. Never compare different profile generations without a compatible reporting method or a recalculated baseline.

## Report format (proposed JSON field inventory)

```json
{
  "format": "daat.alignment-report/1.0.0",
  "subject": "example-external-app",
  "capability_scope": ["example.inventory.read"],
  "pins": {"source": "external.inventory/2.1.0", "target": "target.native/1.0.0"},
  "method_version": "1.0.0",
  "obligations_total": 12,
  "obligations_supported": 12,
  "transformations": {"identity": 8, "alias": 2, "structural": 1, "contextual": 1},
  "burden_points": 8,
  "loss_count": 0,
  "mandatory_unsupported": 0,
  "unresolved_ambiguities": 0,
  "conformance": {"result": "pass", "tck_version": "example-only"}
}
```

Values are **illustrative**, not verified measurements. This object is *not* a published schema until the matching ADR and JSON Schema land.

## Example across versions (hypothetical)

| External app | Supported obligations | Mapping | Burden per obligation | Loss | Conformance |
|---|---:|---|---:|---:|---|
| v1 | 12/12 | aliases + structural + contextual | 8/12 | 0 | pass |
| v2 | 12/12 | aliases only | 2/12 | 0 | pass |
| v3 | 12/12 | exact native | 0 | 0 | pass |

All versions are interoperable and valid for the declared scope. v3 merely needs less **semantic adaptation**. Refactor cost is an application-specific tradeoff and is not guaranteed to decrease monotonically.

## Publishing policy

Offer a private local report by default. Public badges must be opt-in, bounded to verified capabilities/versions and free of sensitive schema information. Avoid pressure-based leaderboards, particularly for independent projects with legitimate reasons to use different models.

## Long-term trend measure

Use a time series keyed by profile version, capability scope and method version: `burden_per_obligation`, `coverage`, `loss_count`, `unsupported_mandatory`, `conformance`. The best evidence of convergence is a **repeatable reduction in mandatory transforms without sacrificing compatibility, ownership or correctness**.
