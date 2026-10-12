# Declarative mapping profiles — design specification

**Status: PROPOSAL.** Existing IK `MappingProfile` Python protocol exposes `id`, `version`, `map_export`. This document designs a safer declarative evolution; implementation MUST preserve the published IK signature through a wrapper, or follow an approved IK contract change.

## Why declarative profiles

Foreign systems often differ legitimately in structure, naming, units, enum vocabulary, representation of uncertainty or source authority. A mapping converts only what can be stated and reviewed explicitly. Profile review should be possible without executing arbitrary application code.

## Proposed mapping pack layout

```text
mappings/<provider>/<profile-id>/<semver>/
  profile.json                 # manifest and lock refs
  transformations.json         # allowlisted operations and field rules
  examples/input.json          # sanitized foreign fixture
  examples/expected.json       # exact native expected fixture
  preservation-report.json     # preserved, derived, excluded and unknown fields
  README.md                    # mapping justification and owner decisions
```

## Proposed `profile.json` shape (ILLUSTRATIVE, not a released contract)

```json
{
  "format": "daat.mapping-profile/1.0.0",
  "id": "external-inventory-to-native",
  "version": "1.0.0",
  "source_contract": {"ref": "external.inventory/2.1.0", "sha256": "<pinned-digest>"},
  "target_contract": {"ref": "target.native/1.0.0", "sha256": "<pinned-digest>"},
  "mapping_rules": "transformations.json",
  "fields": {
    "must_preserve": ["producer_id", "source_revision", "provenance"],
    "may_derive": ["standard_measure_unit"],
    "must_not_infer": ["recognized", "actionability"]
  },
  "loss_policy": "reject_required_loss",
  "conformance_fixture_set": "examples"
}
```

`<pinned-digest>` is a deliberate placeholder. Before any profile is accepted, replace it with a real digest and validate against an approved schema. Do not let AI interpret this illustration as a valid production lock.

## Allowed transform classes

| Class | Examples | Burden level | Preconditions |
|---|---|---|---|
| Identity | field and meaning unchanged | 0 | Exact target semantics demonstrated |
| Safe alias | `purchase_date` → `ordered_at` | 1 | Meanings and timezone policies match |
| Structural | flatten objects, restructure arrays | 2 | No discarded data or changed cardinality |
| Explicit value transform | known unit conversion, exact enum table | 2 | Declared precision, rounding and failure policy |
| Contextual | policy-approved mapping depends on declared context | 4 | Context is provided, versioned and tested |
| Lossy but permitted | drop optional non-critical field | 8 | Owner-approved exclusion with visible loss record |
| Prohibited / unresolved | invent identifier, erase mandatory epistemic qualifier | BLOCK | Human/owner decision required |

This burden table feeds the measurement specification, but the number is **not** a product quality score.

## Transformation DSL requirements

MUST support a finite reviewed set such as `copy`, `rename`, `select`, `construct_object`, `map_enum`, `convert_unit`, `default_if_explicitly_authorized`, `drop_if_optional`, and `assert`. The runtime MUST NOT use unrestricted arbitrary code, network lookups or non-deterministic model calls in mapping expressions. Any extension operation needs versioned review and sandbox/security tests.

Each rule records:

- input path and exact source contract meaning;
- output path and exact target contract meaning;
- transform operator and operands;
- reversibility (yes/no), precision loss, null behavior;
- source attribution and provenance handling;
- tests including invalid, missing, malicious and boundary values;
- justification and approver for any semantic deviation;
- calibration of its burden class.

## Null, unknown, absent and unsupported values

These are **not interchangeable**. Empty text, null, missing field, unknown value, explicit false and not applicable may have different source semantics. Profile must either preserve distinction or reject when mandatory target meaning cannot represent it. Never default missing `recognized` to `true` or actionability to `automatic`.

## Identity/provenance rules

1. Persist foreign identifier in its declared namespace; do not claim it is a Kristall semantic identifier.
2. Attach source revision, timestamp and owner when supplied; do not manufacture them as historical facts.
3. Distinguish author's assertion, adapter's derived expression and receiving owner's validation decision.
4. Reconstruct/forward `ArtifactRef.owner` precisely; DaaT's local journal does not confer ownership.
5. Where a field contains uncertainty, applicability, coordinates or Reader Policy references, use Kristal-approved explicit mapping rules or stop.

## Semantics mapping for existing IK Kristal case

The existing IK upgrade note lists legacy-to-v6 rules such as:

- `structured_epistemic_state` → `kristal_state`;
- `certainty_level` and `uncertainty` → typed `valuations[]`;
- `qualifiers` → `coordinates`;
- `scope` → `applicability`;
- preserve `record_role` / `actionability` where supported.

These are **specific documented compatibility rules**, not permission to run generic inference. Use the exact upstream Kristal contract and test vectors to define each conversion. When ambiguity remains, block or require owner-approved mapping; never fill by intuition.

## Version evolution

Profile versions follow explicit compatibility policy. Any change to a declared field mapping, loss behavior, identity semantics or upstream contract digest creates a new immutable profile release. A change to tests alone does not justify changing historical output for the same locked version.

## Proof of correctness

For each profile provide exact golden-input → golden-output test, loss inventory, changed-field inventory, round-trip test where meaningful, schema checks, provenance checks, and negative/attack test. Report unsupported source fields; do not silently treat them as covered.
