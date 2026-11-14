# 36 — Kristal owner-chain local handoff (DaaT 0.4.1)

**Status:** implemented offline **preflight + local review handoff** only. No owner-approved import, no IK ingress, no canonical KQ/KP/KA/KS mutation, no public release. This is an owner-facing bridge **proposal**, not a released ecosystem wire contract.

## What was inspected

- `Kristal-Framework/VERSION`: `11.0.0-draft.4` in the supplied source snapshot.
- `Kristal-Authoring-Kit/VERSION`: `4.0.0-draft.4`; `contracts/v11-framework-pin.json` pins 13 Framework source files by SHA-256.
- `Kristalizer/BRANCH02_FINAL_SYSTEM_HANDOFF.md`: requires explicit Kit compatibility, accepted KS evidence and staged **copies**; it does not support automatic identity creation or general source-to-domain-claim conversion.
- `Kristal-Authoring-Kit/docs/31_BRANCH02_FINAL_SYSTEM_HANDOFF.md`: canonical authoring authority remains the Kit; Framework defines semantics; diK supplies catalog/crosswalk candidates; each write remains separately gated.
- `diK/README.md` (GitHub): alpha.7 targets Framework **draft.3**. That does not establish safe compatibility with Kit/Framework **draft.4**. Qualification remains blocked.
- `Arketype/AGENTS.md`: design-only archetypes, not semantic authority.
- `kOA-Digital-Ecosystem/docs/target/functional-chains/chains/FC-03`, `FC-04`, `FC-23`: proposals and owner-adopted transfer are separate from local mapping, canonical authoring and IK delivery.

The newly attached `znapshot_kOA_Digital_Ecosystem_11131901.zip` contains a central coordination repository snapshot, **not all independent owner source checkouts**. It cannot prove a current multi-owner integration. The older `SmartDump_20261113_155059.zip` contains Framework, Kit, Kristalizer, Arketype and IK source snapshots. Do not promote snapshot evidence to live qualifications.

## Implemented behavior

1. `kristal-owner-preflight` reads an explicitly supplied common root and optional per-owner roots, checks Kit and Framework versions, all Framework source files declared in Kit's draft.4 SHA-256 pin, and installed Kristalizer/diK/Arketype presence. It never executes owner code. A checksum is local integrity evidence, **not publisher authentication**. The diK draft mismatch remains explicitly unqualified.
2. `kristal-prepare-handoff` requires a valid `daat.local-evidence-preview/0.1.0-prototype` and an exact matching `daat.local-review-packet/0.1.0-prototype`. Only candidates explicitly marked `submit_to_owner` are offered; `reject` / `defer` stay out. Hashes, evidence IDs and source anchors are cross-checked. By default, raw source contents are **not** duplicated. `--include-evidence` is explicit and writes a private local output.
3. `kristal-verify-handoff` validates the prototype packet's local hash and noncanonical status, and can cross-check it against exact preview and review documents.

The local prototype schema lives at [`contracts/daat/kristal-review-handoff.prototype.schema.json`](../contracts/daat/kristal-review-handoff.prototype.schema.json). The output format `daat.kristal-review-handoff/0.1.0-prototype` is **DaaT-local only**. It is not `kristal.build.request/2.0.0`, a diK migration plan, Framework v11 semantic graph, signed Kit approval, or a receiver-owned admission schema. Never submit it directly to a Kit write command or an IK endpoint.

## Example CLI (all offline)

```powershell
# Assuming separate checkouts located directly under C:\mycode.
python -m daat kristal-owner-preflight --root C:\mycode --out C:\mycode\owner-preflight-private.json

# After creating a valid local preview and decisions with existing commands:
python -m daat kristal-prepare-handoff --preview preview.json --review review.json --out proposed-handoff.json
python -m daat kristal-verify-handoff --handoff proposed-handoff.json --preview preview.json --review review.json
```

If checkouts are nested, specify `--framework`, `--kit`, `--kristalizer`, `--dik` and `--arketype` explicitly. No recursive search, no network download, no embedded Kit. Output paths must be in an existing directory. All source files and reviewer packets stay private unless separately and explicitly authorized for disclosure.

## Blocked work for a full source → canonical Kristal chain

- Adopt a **versioned receiving-owner schema** for DaaT review/evidence proposals, with exact bilateral producer/consumer fixtures, source custody permissions and authenticated identity/Konfid decisions.
- Independently qualify diK's draft.3/draft.4 compatibility or migrate under owner-approved contracts; never change pin files to make a check pass.
- Add reviewed domain `KA/KS` construction semantics and validated evidence links in Kristalizer/Kit owner code; current Kristalizer does not bulk-create arbitrary semantic claims from imported documents.
- Pass the real receiver Kit workspace transaction, Framework qualification, replay/recovery and rollback tests before enabling write effects. The receiving Kit must create and validate all canonical records itself.
- Keep qualification, Git/publication, distribution and activation separate. Do not infer access from an owner receipt, checksum, declarative reviewer or Arketype hint.

## Safe next integration milestone

The owner teams should agree on a read-only **producer/consumer test fixture** for the packet and write a separate receiving importer that fails closed. Only then allow a user-confirmed staged workspace import. DaaT itself must remain an interoperability boundary, not another semantic authoring authority.
