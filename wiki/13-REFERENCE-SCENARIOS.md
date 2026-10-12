# Reference scenarios and acceptance narratives

The following are **design/test scenarios**, not evidence of live runtime integration.

## A — Native-shaped external application (zero semantic transformations)

A partner app exports a source-owned record whose identifiers, semantics and fields already match an approved contract. Its DaaT boundary verifies the IK profile, trust, permission, field contract and artifact digest. It forwards/dispatches via the owner-approved port, emits receipt and produces an alignment report with `burden_points=0` for the declared scope. Auth and delivery overhead do **not** count as semantic transformations.

**Negative:** correct schema from a different tenant must be denied.

**Success:** no meaning conversion, correct authorized result, owner-preserving refs, C1–C4.

## B — Independent foreign inventory model (nonzero but conformant)

An external inventory application uses `qty_items` instead of `quantity`, nested unit descriptions and its own product IDs. Adapter maps aliases and structure to a consumer-native read contract. The original product ID remains in the source namespace. If source includes provenance it is preserved; no currency or unit conversion without a declared precise rule.

**Negative:** missing unit with no authorized default causes mapping failure, not fabricated kilograms.

**Success:** burden report lists each rule, loss=0, golden output matches, integration is conformant even though non-native.

## C — Ambiguous knowledge evidence (rejected)

A foreign source submits claims with text labels but without provenance/uncertainty needed by the target Kristal contract. An AI suggests likely identity mappings. DaaT MUST reject or mark as unresolved; cannot issue canonical Kristall identifiers or promote claims to reference status.

**Success:** `MAPPING_AMBIGUOUS` or owner-approved equivalent, no ready artifact, no authority escalation.

## D — Legacy-to-v6 Kristal build (existing reference path)

IK `kristal.build.request/2.0.0` addressed to `daat` carries `mapping_profile`, `requested_outputs`, `kristal_contract_set: "6.0.0"` and source export refs. DaaT validates/adapts to Kristal v6 portable shape. A fake/native Kristal client returns source-authorized artifact references. Output validation and IK receipts/events follow the actual owner contract. v7 meta-only material is never injected into the v6 Profile.

**Success:** accepted by actual IK owner validators, lock passes, provenance and ownership unchanged.

## E — Orgo event from foreign task tool

An external ticket system reports completion. Its DaaT pack may map an event onto an **owner-approved IK/Orgo event profile**. Orgo decides whether the task is complete. DaaT cannot declare mission closure by matching a string. This case **must wait** until there is an accepted specific IK/Orgo profile and authority policy.

**Success:** verified sender, stable source task ID, exact mapping, Orgo owner performs any operational transition.

## F — External educational media gallery

A foreign gallery wants to publish an artwork belonging to a pupil. DaaT checks owner-issued publication authorization and compatible public artifact metadata. Without affirmative authorization, publication is blocked; do not merely blur a public copy or reveal tags/locators. DaaT does not hold originals or grant consent.

**Success:** private source remains private, safe status receipt; positive case only with verified owner publication policy.

## G — Adapter convergence sequence

An external app at v1 needs aliases, unit conversion and structural transforms. At v2 it adopts target field semantics, leaving only an alias; at v3 output is directly native-shaped. Under the **same capability scope and metric method**, mapping burden declines. Conformance stays `pass` throughout if all tests pass. This is the voluntary incentive.

**Success:** transparent historical reports, no leaderboard, no false claim that v1 app is inferior.
