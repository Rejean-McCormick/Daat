# DaaT 0.4.2 — kOA C0 checkout paths and diK schema parity

**Classification:** `LOCAL_IMPLEMENTED` for read-only location resolution and schema byte comparison; `BLOCKED` for owner acceptance, semantic identity registration, real IK routing and publication. No owner canonical state is modified.

## Source of the local path list

The supplied 2026-11-13 `SmartDump_20261113_191237.zip` contained 14 independently captured source trees. In `kOA_Digital_Ecosystem/docs/inventory/repositories.json`, the C0 coordination project declares each repository's **Windows local checkout path**. That is the source of path hints, **not a proof of repository identity, a signature, or authorization to access source bytes**.

DaaT reads the inventory only from the selected root's exact location `kOA_Digital_Ecosystem/kOA_Digital_Ecosystem/docs/inventory/repositories.json` (or a path explicitly provided using `--inventory`). The file must be inside the selected root, be a regular file, contain bounded JSON, and have no duplicate recognized owner identity. It accepts only `C:\mycode\...` path declarations, then relocates their suffix under the caller's `--root`. This is **not a recursive file search** and does not follow symlinks for owner pin files.

## Actual documented checkout paths

```text
C:\mycode\Interaction-Kernel\Daat
C:\mycode\Interaction-Kernel\interaction_kernel
C:\mycode\Kristal\Kristal-Framework
C:\mycode\Kristal\Kristal-Authoring-Kit
C:\mycode\Kristal\Kristalizer
C:\mycode\Kristal\Arketype\arketype
C:\mycode\diK\diK
C:\mycode\Skope\Skope
C:\mycode\kOA_Mediatheque\mediatheque
C:\mycode\kOA_Mediatheque\mediatheque-blank
C:\mycode\Konfid\konfid
C:\mycode\Kristal\Kristal-Integration-Pack
C:\mycode\Kristal\Kristal-Manager
C:\mycode\kOA_Digital_Ecosystem\kOA_Digital_Ecosystem
```

## Available read-only commands

From a correctly installed DaaT 0.4.2 Python environment:

```powershell
python -m daat kristal-owner-locations --root C:\mycode
python -m daat kristal-owner-preflight --root C:\mycode --out C:\mycode\daat-owner-preflight.private.json
```

The first command reports the inventory's SHA-256 and mapped local paths; it does **not** assert they exist, are authentic, belong to the caller or are entitled to access. The second checks Framework/Kit versions, Kit's 13 Framework source pins, Kristalizer presence and the diK v11 schema equality, with any available components only. The optional report should be kept private: it contains absolute local paths.

### What was checked in the provided source snapshots

- Framework: `11.0.0-draft.4`, semantic KQ/KP/KA/KS model.
- Authoring Kit: `4.0.0-draft.4`, pinned Framework files; **only the Kit** registers canonical graphs.
- diK: `1.0.0a7` declares Framework `draft.3` in its README, while its bundled 11 schemas can be compared byte-for-byte against the `draft.4` Framework source. Byte equality **does not establish functional/semantic compatibility or permit import**.
- Kristalizer: `1.2.2`, orchestrates proposals and independent Kit workspaces; it expressly does not bulk-create arbitrary domain KA/KS facts.
- Skope/EncyK and Médiathèque: acquisition and custody are owner-controlled. A source handoff/receipt is not a Kristal authoring permission.
- IK: previous v6 `kristal.build.request/2.0.0` cannot be repurposed as generic third-party ingress.
- Konfid: user/workload proof and policy enforcement remain host-owner responsibilities, not something DaaT may manufacture from local paths or a review name.

## Remaining owner contract gates

1. Independently run and qualify the real producer/consumer fixture for diK alpha.7 → Kit `import-dik-catalog` on disposable workspaces; preserve their explicit transaction/recovery rules.
2. Obtain an **approved Kit receiving profile** for DaaT proposals. DaaT's `daat.kristal-review-handoff/0.1.0-prototype` is not that profile.
3. Bind a source custody permission, an authenticated actor, a current Konfid decision and receiving-owner access rules to any real import.
4. Validate domain-specific semantic assertions with existing KQ/KP/KA/KS evidence and independent qualification; no label-based `exactMatch`.
5. Preserve the separate admission, build, independent qualification, publication and activation decisions.

## Testing boundary

DaaT's local tests cover C0 inventory parsing, path traversal rejection, duplication, diK schema parity and mismatch. They do not run an owner Kit transaction, produce signed receipts, or certify deployment. The C0 inventory is read-only and never copied as an authority contract.
