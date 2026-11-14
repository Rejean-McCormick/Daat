# DaAT 0.4.3 — Local chain audit and review validation

**Status:** `IMPLEMENTED_LOCAL_ONLY`; no IK/Kit/Konfid receiver contract is adopted.

- `daat kristal-local-chain-audit --preview PREVIEW.json --review REVIEW.json --handoff HANDOFF.json [--root C:\\mycode] [--out AUDIT.json]` checks all three artifacts and their exact references; optionally runs read-only Framework/Kit/diK pin preflight.
- The audit contains digests, counts and decisions, **not** original source records. Its SHA-256 is a local integrity check, not a signature.
- `verify-review` now refuses undeclared fields, duplicate/invalid candidate IDs, malformed evidence IDs and recomputed-hash authority tampering.
- `verify-handoff` now validates each submitted item's typed evidence and noncanonical design hints, and requires both or neither paired artifact.
- No direct owner invocation, global ingress profile, publishing, identity minting, source-byte permission or Kit workspace change.

## Qualification still required

The owner of the Kit must adopt a versioned receiver contract and both sides must test real positive, negative and replay fixtures. Interaction Kernel, Konfid, Skope and Médiathèque require their own separately approved bilateral admission and execution evidence. No local checksum supersedes such approval.
