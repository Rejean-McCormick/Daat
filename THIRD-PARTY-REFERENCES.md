# DaaT Kintsugi components — credits and redistribution policy

**Status:** Documentary reference list, not a license clearance or bundled software inventory.

| Project | Upstream | Use | Relationship |
|---|---|---|---|
| Git | https://git-scm.com/ | Local pinned tree/blob reads via installed executable | Host prerequisite, not bundled |
| pypdf | https://github.com/py-pdf/pypdf | Local PDF text per page | Optional Python extra, not bundled |
| jsonschema | https://github.com/python-jsonschema/jsonschema | JSON schema validation | Existing Python package dependency |
| Singer/Meltano SDK | https://sdk.meltano.com/ | Extractor contract inspiration | Reference only; not installed |
| Docling | https://github.com/docling-project/docling | PDF tables/OCR potential sidecar | Reference / optional future Annex |
| OpenRefine | https://openrefine.org/ | Review and reconciliation workflow inspiration | Mimic concept / optional future Annex |
| Apache Tika | https://tika.apache.org/ | Optional broad file parsing | Reference only |
| Debezium | https://debezium.io/ | Possible future DB change streams | Reference only |
| dlt | https://dlthub.com/ | Possible future bounded bulk handling | Reference only |

When distributing a build that contains third-party programs, record actual pinned versions, SPDX IDs, copyright/NOTICE files, transitive dependencies, models and separate source-data permissions. This table does not assert exact legal license terms; check official notices for every installed version. Pure pattern inspiration must credit upstream without claiming code reuse or official endorsement. DaaT's own `LICENSE-POLICY.md` still requires owner decision.
