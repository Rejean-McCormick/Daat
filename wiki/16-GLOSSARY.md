# Glossary — precise terms

**Alignment (native contract alignment):** source application already represents the needed meaning according to the target's declared, versioned contract. Does not imply identity or authorization equivalence.

**Admission:** local boundary decision to accept a well-formed, authenticated and authorized interaction for processing. Different from transport delivery or semantic recognition.

**Adapter:** application-specific mapping/profile/connector code at a boundary. It may be small or extensive without implying application quality.

**Alignment distance / mapping burden:** quantified amount of declared semantic adaptation required for a specific capability+contract scope. Not total code lines or a universal quality score.

**ArtifactRef:** IK standard reference to an owner-controlled artifact (`owner`, `artifact_type`, `artifact_id`, optional version/integrity/etc.). Pointer, not ownership transfer.

**Conformance:** demonstrable satisfaction of an explicit scoped contract and test suite, independent of adaptation burden.

**Contract owner:** system/project authorized to version the source or target schema and define its semantics.

**DaaT:** named external admission/anti-corruption boundary; technical system identifier `daat`. Existing IK usage is Kristal-focused; broader external integration is a proposed extension.

**Epistemic validation:** examination of evidence/knowledge claims under domain criteria; not performed automatically by IK admission or mapping.

**ExportManifest:** IK structured description of a source-owned immutable export/snapshot with item refs and integrity.

**IK / Interaction Kernel:** cross-system interaction transport, envelopes, profiles and receipts; not a shared semantic authority.

**Kristal / Kristall:** knowledge structure and related meta-artifact standards; semantic identity/provenance/recognition remain owner-owned.

**Mapping profile:** reviewed, pinned declaration of an adaptation from one exact contract version to another.

**Native-shaped external system:** external participant using target meaning without semantic transformations, still subject to boundary security.

**Orgo:** owner of operational orchestration and mission/task transitions; DaaT is not a workflow engine.

**Owner-native connector:** minimal interface that calls the system actually responsible for the requested operation.

**Portable v6 Kristal:** existing `kristal_state/6.0` exchange representation, maintained unchanged under additive Kristal v7 model.

**Profile:** IK's explicit versioned interaction contract. DaaT mapping profile is a distinct concept; keep naming clear.

**Source owner:** system responsible for original data, mutable operational state and source evidence; DaaT does not become this owner.

**Transform inventory:** explicit report of each mapping step with reasons, inputs/outputs and loss/preservation classification.

**Zero semantic transformation:** boundary processing without changes to the meaning-carrying structure for a declared capability. **Not** zero authentication, zero validation, zero transport or zero cost.
