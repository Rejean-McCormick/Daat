# Guide for an external application integrating through DaaT

DaaT invites systems to join **without rewriting their internal architecture**. The alignment report describes *integration effort*, not whether their app is good or bad.

## Step 1 — Declare a narrowly scoped capability

Choose one operation, for example `inventory.read` or `order.status.notify`. Describe:

- operation direction, sender, receiver and owner of data;
- normal source schema and version (existing native app representation, not a specially pretranslated export);
- permitted tenant(s), actor authority, data sensitivity and trust method;
- transport surface (IK profile/capability if approved);
- exact external and target contract versions.

Do not attempt to map an entire ERP or medical/school platform in one broad profile.

## Step 2 — Pin versions and collect fixtures

Prepare two sanitized fixtures: valid and invalid boundary input. Provide a source-owned immutable snapshot or ExportManifest with integrity hashes. Reference the exact owner-supplied IK and target contracts. All sensitive examples use synthetic identities.

## Step 3 — Try the zero-transform route first

Validate the application's original output directly against the target schema and semantic obligations. If valid **and** meanings/identity/authorities align, no semantic mapping is needed. DaaT remains responsible for boundary admission and traceability.

## Step 4 — Declare only necessary differences

For each mismatch, classify:

- field alias only;
- structure or unit representation;
- vocabulary requiring an explicit lookup table;
- ambiguous meaning requiring source-owner input;
- unsupported or lossy field requiring refusal or documented owner approval.

Do not assume equivalent labels imply equivalent meaning. Keep the foreign app's native object untouched whenever possible.

## Step 5 — Build reviewed mapping pack

Follow [Mapping Profiles](06-MAPPING-PROFILES.md). Provide positive, boundary, negative and malicious tests. Define null/missing values, precision/rounding and provenance preservation. Prefer source-correct contracts over a clever mapping if the developer *wants* to align, but do not force migration.

## Step 6 — Configure trust and admission

The sending system's identity is provisioned by the appropriate trust provider. The receiver validates authority; DaaT must not assume a valid structure grants access. Scope credentials by tenant, capability, audience, and lifespan.

## Step 7 — Run four conformance tracks

See [Conformance](09-CONFORMANCE-AND-TESTS.md). Run real IK contract validation, golden mapping tests, security negatives and owner integration tests. A dry run or mock does not prove production readiness.

## Step 8 — Obtain an alignment report

Report exact contract scope, versions, coverage, transformation classes, any loss, and TCK results. A conformant integration may require significant adaptation. The report highlights which differences could be eliminated if the app evolves.

## Step 9 — Evolve voluntarily

If the app introduces canonical field names or adopts semantic identifiers properly, create a *new* application version and DaaT mapping version. Re-measure the same capability scope; archive prior reports. No secret adapter rewrites.

## Minimal integration checklist

- [ ] Receiver/profile owner approves intended capability.
- [ ] Source and target schema references are immutable and integrity pinned.
- [ ] Normal native-output fixture is available and sanitized.
- [ ] Trust and tenant boundaries are configured and tested.
- [ ] Mapping is deterministic and explicitly reviewed.
- [ ] Identity, provenance and source ownership survive.
- [ ] Output is owner-validated; an IK Receipt/Event is correctly correlated.
- [ ] Failure and duplicate delivery behavior are tested.
- [ ] Public report is opt-in and non-sensitive.
- [ ] Version migration path is documented.

## Frequently misunderstood points

**Must we use Kristal internally?** No. An external app can keep its model and adapt at the boundary. Exact downstream contract and authority depend on the requested capability.

**Does a larger adapter mean we failed?** No. It means the integration uses more mapping steps in the declared scope. It can still fully conform.

**Can we bypass DaaT when already aligned?** The architecture supports a **minimal** DaaT boundary for externally joining apps. Internal native-to-native exchanges need no extra semantic translation; admission may still be enforced by IK/owner paths.

**Can the DaaT mapper infer a missing fact using AI?** No at runtime. A tool may propose candidate mappings for human review; unreviewed mappings and invented claims must not cross the production boundary.
