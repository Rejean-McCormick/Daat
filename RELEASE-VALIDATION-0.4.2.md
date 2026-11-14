# DaaT 0.4.2 — local source-alignment release evidence

**Scope:** source code snapshot alignment and local read-only safeguards; pre-production. Owner integration/publish authority remains blocked.

## Exact source snapshot supplied

`SmartDump_20261113_191237.zip` contained 14 independent checkout snapshots and file indexes. The central C0 repository source contains `docs/inventory/repositories.json`. The DaAT source in this SmartDump is **v0.3.0**, so this release extends the separately developed DaAT **v0.4.1** source tree; the old SmartDump DaAT copy was used solely to check owner documents and paths, not to replace later code.

## Implementation added

- Exact C0 `C:\mycode` path mapping (no arbitrary disk search), with explicit override capability and tampering denials.
- A bounded `kristal-owner-locations` read-only CLI command.
- A byte-exact local parity comparison for diK alpha.7's 11 vendored Framework v11 schemas, matching the scope of the Kit Branch02 checker; no writes, no subprocess or network calls.
- Explicit draft.3→draft.4 **functional qualification blocker remains in place**, even when all 11 schema files match.
- Tests for duplicate identity, path escape, unexpected diK version and schema alteration.

## Authority limits

A clean C0 inventory, pin, schema, or unit test **never** authorizes source disclosure, imports, KQ/KP/KA/KS registration, public Git, host activation or a Konfid policy decision. The DaAT local proposal remains `daat.kristal-review-handoff/0.1.0-prototype`, **not** a Kit receiver contract.

## Final checks

Executed after the code was frozen on the supplied snapshots:

- `PYTHONPATH=src python -m pytest -q` — **165 passed**, exit 0 (v0.4.1 baseline: 153).
- `PYTHONPATH=src python -m daat verify-contracts` — verified, **9 IK v6 pinned files**, exit 0; old v6 scope only.
- `python tools/check_markdown_links.py` — **129 relative links** checked, exit 0.
- DaAT owner preflight on exact snapshot paths (explicit overrides) — **Framework/Kit 13-file pin exact, no drift; diK 11 schema bytes match; Kristalizer 1.2.2**; status remains **blocked**, not approved.
- Kit-owned `scripts/check_branch02_interop.py --framework ... --dik ...` — exit 0; `framework_reference_coverage_match=true`, `canonical_workspace_modified=false`, `approved_to_publish=false`; only local source compatibility, not full TCK.
- `kristal-owner-locations` against the actual C0 inventory bytes from the new snapshot — exit 0, **14 paths** returned, never considered permissions.

**No real Skope/Médiathèque source handoff, authenticated Konfid service, approved IK generic ingress, adopted Kit DaaT receiver, canonical authoring, publication or activation was tested.**
