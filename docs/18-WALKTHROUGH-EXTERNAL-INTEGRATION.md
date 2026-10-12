# Full conceptual walkthrough — external provider to owner-native operation

**Status:** architectural example, deliberately not a claim of executable current code.

## Context

A foreign inventory app called `supply-bridge` uses an independent inventory domain. An authorized partner wants to expose a **read-only stock snapshot** to a consumer in the ecosystem. This is a hypothetical capability; a named IK profile and recipient API must be accepted by their contract owners **before** actual execution.

### Source record (synthetic example)

```json
{
  "id": "stock-27",
  "facility": "warehouse-example",
  "qty_items": 24,
  "measure": {"symbol": "pcs", "precision": 0},
  "revision": "rev-8",
  "captured_at": "2026-10-12T12:00:00Z"
}
```

The mapping author declares an exact interpretation for `qty_items`, `measure.symbol`, revision and source ownership. It does **not** invent a supply chain company's identity or attest real stock facts.

## Stage 0 — Owner/scope agreement

Target system approves a capability, target schema and authority policy. Source app agrees to export. Both versions/digests are pinned. No operation proceeds from just a JSON sample.

## Stage 1 — Authenticated interaction

IK receives an interaction with explicit source, target, profile, subject, correlation, authority and artifact references as required by that approved capability. Schema validation and trust checks occur before mapping. An aligned data shape is not a bypass.

## Stage 2 — Source integrity

Check source-owned immutable snapshot or ArtifactRef integrity and tenant scope. A DaaT request never becomes a license to read arbitrary URLs or internal network addresses.

## Stage 3 — Profile and transformation selection

Mapping pack version `supply-bridge-stock/1.0.0` is selected by exact approved contract edge. Its rule inventory might be:

| Source | Target | Operation | Burden |
|---|---|---|---:|
| `qty_items` | `quantity` | safe alias after meaning proof | 1 |
| `measure.symbol` | `unit_code` | enumerated `pcs` mapping | 2 |
| `revision` | `source_revision` | alias | 1 |
| `captured_at` | `observed_at` | alias and timezone-preserving | 1 |
| `id` | `source_record_id` | preserve original namespace | 1 |

`burden_points=6` in this illustration; measure covers only the declared obligations and reviewed transforms. The system may be fully conformant despite that burden.

## Stage 4 — Native recipient handoff

DaaT generates a validated native *input* under the owner-approved target schema and calls an owner-native connector. The recipient owns any state and the interpretation of the stock record. DaaT has no authority to change a warehouse's real quantity.

## Stage 5 — Output, ownership, event and receipt

Recipient returns its permitted result or reference. DaaT verifies shape, integrity, owner and authorization, then sends IK receipt/event according to that profile. Do not claim `kristal.artifact.ready` for a stock record unless a legitimate **Kristal build** actually occurred under that separate profile.

## Stage 6 — Reproducible report

Publish a private alignment report listing all obligations and rules, no loss and exact source/target/mapping versions. Show how a later source release using matching target fields might reduce semantic transform burden. No recommendation to alter its independent internal model is mandatory.

## Five rejection tests

1. Source claims tenant B using tenant A credential → deny.
2. Target version unsupported → reject, no lossy best-effort translation.
3. Source unit ambiguous (`box` without package count) → stop, do not guess.
4. Sender retries with same idempotency key and changed quantity → conflict; no duplicate effect.
5. Source URL points to local metadata service → reject locator without request.

## What is needed for a real demo

- Approved exact generic IK profile + receiver schema.
- Real trust provider in isolated environment.
- Valid source ExportManifest/ArtifactRef or approved equivalent.
- Mapping pack JSON Schema and interpreter built under the DaaT ADR.
- Native connector test double and then real owner endpoint.
- Output validation, receipt correlation and TCK evidence.

Until these exist, this is a *worked design example*, not a working implementation.
