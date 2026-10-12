# DaaT — GitHub Wiki

**Interoperability without enforced uniformity.** A minimal or extensive DaaT adapter can connect an external application. The mapping burden expresses scoped distance from shared contracts, never application quality.

**Status:** documentation specification only; an IK Kristal reference adapter exists, but a generic DaaT service is not yet demonstrated.

## Documentation

- [Document status](00-DOCUMENT-STATUS.md)
- [Upstream evidence](01-SOURCE-BASELINE.md)
- [Vision & invariants](02-VISION-AND-INVARIANTS.md)
- [Architecture](03-ARCHITECTURE.md)
- [Contracts & versions](04-CONTRACTS-AND-VERSIONS.md)
- [Security](05-ADMISSION-AND-SECURITY.md)
- [Mapping profiles](06-MAPPING-PROFILES.md)
- [Alignment metrics](07-ALIGNMENT-METRICS.md)
- [Runtime](08-RUNTIME-AND-LIFECYCLE.md)
- [Conformance / TCK](09-CONFORMANCE-AND-TESTS.md)
- [Developer guide](10-EXTERNAL-DEVELOPER-GUIDE.md)
- [Implementation plan](11-IMPLEMENTATION-PLAN.md)
- [Operations](12-OPERATIONS.md)
- [Scenarios](13-REFERENCE-SCENARIOS.md)
- [Open decisions](14-OPEN-DECISIONS.md)
- [AI build backlog](15-AI-BUILD-BACKLOG.md)
- [Glossary](16-GLOSSARY.md)
- [Cross-repo changes](17-INTER-REPOSITORY-CHANGE-MATRIX.md)
- [External walkthrough](18-WALKTHROUGH-EXTERNAL-INTEGRATION.md)
- [French vision](00-French-Vision.md)
- [AI coding instructions](AGENTS.md)
- [ADR DaaT purpose](ADR-0001-DAAT-PURPOSE.md)
- [ADR measurement](ADR-0002-ALIGNMENT-MEASUREMENT.md)
- [ADR IK governance](ADR-0003-IK-PROFILE-GOVERNANCE.md)

## Executable offline alpha

The current repository includes an executable local library and CLI. See [Implementation Status](19-IMPLEMENTATION-STATUS.md) for tests, boundaries and open integration decisions.

## Security boundary v0.3

- [Security enforcement boundary](20-SECURITY-BOUNDARY)
- [Konfid contract alignment](21-KONFID-CONTRACT-ALIGNMENT)
- [External mapping API](22-EXTERNAL-MAPPING-GUIDE)
- [Threat and trust matrix](23-THREAT-AND-TRUST-MATRIX)

**Status:** local Python security gates tested; no production IdP, Konfid transport, audit broker or IK external ingress endpoint shipped.
