# DaaT architecture and implementation documentation

These files form the **canonical build specification** for DaaT. They are intended for human engineers and AI implementation agents; this release ships **no operational DaaT runtime**.

Read order:

1. [Source baseline and factual status](01-SOURCE-BASELINE.md)
2. [Vision/invariants](02-VISION-AND-INVARIANTS.md)
3. [Architecture/ownership](03-ARCHITECTURE.md)
4. [Contracts/versions](04-CONTRACTS-AND-VERSIONS.md)
5. [Admission/security](05-ADMISSION-AND-SECURITY.md)
6. [Mapping profiles](06-MAPPING-PROFILES.md)
7. [Alignment metrics](07-ALIGNMENT-METRICS.md)
8. [Runtime/delivery](08-RUNTIME-AND-LIFECYCLE.md)
9. [TCK/tests](09-CONFORMANCE-AND-TESTS.md)
10. [Developer guide](10-EXTERNAL-DEVELOPER-GUIDE.md)
11. [Implementation plan](11-IMPLEMENTATION-PLAN.md)
12. [Operations](12-OPERATIONS.md)
13. [Reference scenarios](13-REFERENCE-SCENARIOS.md)
14. [Open owner decisions](14-OPEN-DECISIONS.md)
15. [AI build backlog](15-AI-BUILD-BACKLOG.md)
16. [Glossary](16-GLOSSARY.md)
17. [Inter-repository change matrix](17-INTER-REPOSITORY-CHANGE-MATRIX.md)
18. [External walkthrough](18-WALKTHROUGH-EXTERNAL-INTEGRATION.md)

For strict AI implementation constraints, see [../AGENTS.md](AGENTS.md). For a French expression of the product intent, see [fr/VISION.md](00-French-Vision.md). ADRs in [decisions/](ADR-0001-DAAT-PURPOSE.md) are **proposed**, pending owner approval.

**Normative precedence:** approved upstream owner contracts/ADRs > approved DaaT ADRs > DaaT documentation examples > unapproved illustrative pseudo-contracts. When versions disagree, stop and record the conflict.
