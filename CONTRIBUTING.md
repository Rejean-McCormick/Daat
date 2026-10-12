# Contributing to DaaT

DaaT is a boundary for interoperable **external systems**, not an opportunity to redefine canonical semantics. Contributors may propose mapping profiles, compatibility fixtures, docs, tests and owner-approved connectors.

Before a change: read `AGENTS.md`, `docs/01-SOURCE-BASELINE.md`, `docs/02-VISION-AND-INVARIANTS.md`, and the exact relevant upstream contracts. All new profiles must declare immutable versions and contract digests, exact source/target obligations, identity/provenance handling, allowed losses and negative tests. Mapping PRs need approval from the affected contract owners. Changes to IK profile semantics go in IK; changes to Kristal meanings go in Kristal, never hidden in this repository.

Use an issue or proposed ADR for contract gaps. Never commit credentials, private user/pupil data, unlicensed corpora or real source documents. Explain the tested behavior, unknowns, source status and compatibility matrix. Avoid presenting prototypes or reference adapters as deployed production services.
