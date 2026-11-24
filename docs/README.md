# DaaT architecture and implementation documentation

These files form the **canonical build specification** for DaaT. They are intended for human engineers and AI implementation agents; DaaT v0.5.0 includes a **local information-bridge implementation candidate**, alongside earlier offline Python library/CLI commands; it is **not** a deployed external integration service. For the current path, see [0.5.0 implementation](pont-information/IMPLEMENTATION-0.5.0.md). [19](19-IMPLEMENTATION-STATUS.md) records an earlier implementation baseline.

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

For strict AI implementation constraints, see [../AGENTS.md](../AGENTS.md). For a French expression of the product intent, see [fr/VISION.md](fr/VISION.md). ADRs in [decisions/](decisions/) are **proposed**, pending owner approval.

**Normative precedence:** approved upstream owner contracts/ADRs > approved DaaT ADRs > DaaT documentation examples > unapproved illustrative pseudo-contracts. When versions disagree, stop and record the conflict.

## v0.3 security runtime addendum

- [20 — Security enforcement boundary](20-SECURITY-BOUNDARY.md)
- [21 — Konfid and kOA contract alignment](21-KONFID-CONTRACT-ALIGNMENT.md)
- [22 — Secure external mapping API](22-EXTERNAL-MAPPING-GUIDE.md)
- [23 — Threat and trust matrix](23-THREAT-AND-TRUST-MATRIX.md)

All four describe implemented local gates and outstanding owner integrations. No IK external ingress schema is invented here.

- [24 — Release evidence](24-RELEASE-EVIDENCE.md)

<!-- daat-universal-onramp-docs-2026-11-13 -->
## Universal external-data onramp — final design / coding baseline (2026-11-13)

**Status:** `TARGET_DESIGN` for the architecture in this section; the 0.3.0 library described in [19](19-IMPLEMENTATION-STATUS.md) is an **earlier** implementation baseline. The current 0.5.0 local bridge candidate is described [here](pont-information/IMPLEMENTATION-0.5.0.md). These additions **do not** adopt a new IK wire profile, source custody API, v11 Kit runtime or production service.

- [26 — Universal onramp: vision and ownership](26-UNIVERSAL-DATA-ONRAMP.md)
- [27 — Source taxonomy and 36-family registry](27-SOURCE-TAXONOMY-AND-REGISTRY.md)
- [28 — Kintsugi/Kompendio open-source integration](28-KINTSUGI-OSS-INTEGRATION.md)
- [29 — User journey, processing and handoffs](29-PROCESS-AND-HANDOFFS.md)
- [30 — Native Kristal standards and provenance](30-KRISTAL-STANDARDS-AND-PROVENANCE.md)
- [31 — Four pilot playbooks](31-PILOT-PLAYBOOKS.md)
- [32 — Tests, negative cases and threat gates](32-TEST-AND-THREAT-PLAN.md)
- [33 — Coding roadmap and owner decisions](33-CODING-ROADMAP.md)
- [34 — Source and owner traceability](34-OWNER-SOURCE-TRACEABILITY.md)
- [Proposed ADR-0004 — Universal onramp/Kintsugi](decisions/ADR-0004-UNIVERSAL-ONRAMP-KINTSUGI.md)

The [36-family exploratory CSV](data/source-family-landscape-36.csv) is a research catalogue, not a claim that connectors are shipped or that their data may be copied. Future external integrations require exact producer/consumer owner contracts and qualification.

## Historical offline source-preparation code (0.4.x; retained in 0.5.0)

- [35 — Implemented offline source-to-candidate CLI and owner blockers](35-OFFLINE-ONRAMP-IMPLEMENTATION-0.4.md)

- [36 — Kristal owner-chain local handoff](36-KRISTAL-OWNER-CHAIN-LOCAL-HANDOFF.md) (v0.4.1; offline, not an approved owner importer).

- [37 — C0 local paths and diK schema-parity limits](37-C0-INVENTORY-AND-DIK-SCHEMA-PARITY.md)

## Pont universel d'information — conception intégrale (2026-11-14)

- [Dossier directeur complet : sources → contexte ChatGPT, sans construction Kristal](pont-information/00-INDEX-ET-STATUT.md).
- [Plan de réalisation intégrale, livraison unique](pont-information/15-PLAN-DE-REALISATION-INTEGRALE.md).
- [Registre exhaustif des 89 plateformes](pont-information/04-REGISTRE-89-PLATEFORMES.md) et [36 familles](pont-information/05-COUVERTURE-36-FAMILLES.md).
- [Contrat local contextuel illustratif](pont-information/08-DOSSIER-CONTEXTUEL-CHATGPT.md), [sécurité et droits](pont-information/10-SECURITE-DROITS-ET-CONFIANCE.md) et [tests d'acceptation](pont-information/14-TESTS-ET-DEFINITION-DE-TERMINE.md).

**Statut** : cible `[PROPOSAL]`, pas une nouvelle livraison de connecteurs. Aucun profil IK, licence de source, droit de transmission ChatGPT ou construction de Kristal n'est accordé par ces documents.
