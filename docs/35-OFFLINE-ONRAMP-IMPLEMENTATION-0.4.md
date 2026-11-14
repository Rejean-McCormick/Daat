# 35 — DaaT 0.4.0 offline source-preparation implementation

**Classification:** `IMPLEMENTED_OFFLINE` for the named Python modules **only**. This page does not amend, adopt or supersede owner APIs, contracts or ADRs. See [33 — Roadmap](33-CODING-ROADMAP.md) and [19 — v0.3 historical status](19-IMPLEMENTATION-STATUS.md).

## Implemented scope

DaaT 0.4.0 adds a **bounded noncanonical source → evidence → review candidate** path to the existing v0.3 mapping/security/IK-v6 build-boundary library. Its files are native local metadata, not a new Interaction Kernel or Kristal wire schema.

| Capability | Code | Actual boundary |
|---|---|---|
| 36 research families and eight-lane catalogue | `catalog.py`, `resources/data/*.csv` | Metadata only; does not grant rights or imply 36 working connectors |
| Source-shape diagnosis | `diagnosis.py` | Suggestions by extension/magic or `.git`; not semantic classification or permissions |
| Strict adapter metadata, registry | `registry.py`, `contracts/daat/adapter-manifest.schema.json` | No untrusted code imports; host injects external workers |
| Explicit selected root and user-rights assertion | `source.py` | This does **not** authenticate source ownership or external API grants |
| Dataset reader | `connectors/common.py` | UTF-8 CSV/TSV/JSON/JSONL, bounded local snapshots |
| PDF | `connectors/pdf.py` | Local, optional `pypdf`; no OCR or Docling installed automatically |
| ZIP archive | `connectors/archive.py` | Local bounded safe entry reader; no extraction or nested ZIP |
| Git | `connectors/git.py` | Immutable full commit only, read-only `git` plumbing; no fetch/checkout/submodule execution |
| Bibliography | `connectors/bibliography.py` | **Local authorized metadata** JSON, JSONL, CSV, RIS, OAI/Dublin Core-style XML; no live provider harvesting |
| Acomba | `connectors/acomba.py` | Typed private **exports** (not direct ODBC/SDK or operational ledger writes) |
| Candidate classification, optional AI review hook | `candidates.py` | Only noncanonical design hints and explicitly untrusted model suggestions |
| Local review packet | `review.py` | No Kit approval, semantic identity grant or publication authority |
| Hosted read provider SPI | `hosted.py` | Only injectable authenticated provider, verifiers, Konfid-shaped policy + audit; no public transport |
| Private preview writer and integrity inspection | `output.py`, `verification.py` | Local content hash, not a Kristal signature/provenance exporter |
| SQLite preview intent journal | `journal.py` | Preview metadata only; not an IK outbox or side-effect replay |

**Stable pre-existing functions:** `daat map`, `validate-mapping`, `alignment-report`, `verify-contracts`, `validate-ik`, `validate-build`, and `V6BuildBridge` remain separate v0.3 APIs; source preparation does **not** call the v6 build bridge or reinterpret its restricted sender profile.

## Local command examples

Install in an isolated Python environment:

```powershell
cd C:\mycode\Daat
python -m pip install -e '.[dev,pdf]'
python -m daat list-source-families
python -m daat list-adapters
python -m daat diagnose-local --help
```

Prepare a small JSONL/CSV snapshot only if you have rights to do so:

```powershell
python -m daat prepare-local --root 'C:\mycode\data' --source 'research.jsonl' --kind dataset --family 07 --tenant 'sample-tenant' --actor 'sample-user' --purpose 'local-research' --license 'owner-granted' --rights-acknowledged --out 'C:\mycode\local-preview.json'
python -m daat verify-local-preview 'C:\mycode\local-preview.json'
```

Other modes: `--kind pdf --family 08`, `--kind archive --family 09`, `--kind git --family 11 --commit <40-hex-full-SHA>`, `--kind bibliography --family 01`, `--kind acomba --family 13 --record-type invoices`. Check CLI help for flags. A Git source is a **relative directory** under `--root`; other sources are relative files. Network URLs are not accepted by `prepare-local`.

An existing preview is never overwritten without `--replace`. Extracted source data is **not printed** to console; the private file, if requested, is your own responsibility to secure, retain and delete. Do not commit private previews to Git. The `--rights-acknowledged` flag is a **local declaration only**, never proof of a source-owner permission or legal right to redistribute.

For review, write a JSON array of explicit decisions with keys `candidate_id`, `decision` (`submit_to_owner`, `reject`, `defer`), `reason`, then use `daat prepare-review preview.json decisions.json --reviewer ... --purpose ... --out review.json`. This remains a **proposal** even when a reviewer selects `submit_to_owner`.

## Kintsugi OSS posture and credits

No third-party code is copied into the DaaT source tree by the new reader modules. **pypdf** is an *optional separately installed* PDF extraction dependency: repository [pypdf](https://github.com/py-pdf/pypdf); verify the exact version, license and dependency notices before redistributing a built environment. The Git connector invokes the locally installed **Git** executable (not included here); [git-scm.com](https://git-scm.com/). The existing Python **jsonschema** dependency remains declared in `pyproject.toml` and requires its applicable notices when redistributed.

Docling, Meltano/Singer, OpenRefine, Tika, NiFi, Debezium and others remain Kintsugi **reference/optional future Annex candidates**, **not** bundled or qualified as runtime components. [28 — Kintsugi approach](28-KINTSUGI-OSS-INTEGRATION.md) owns the planned credit/license workflow. Attribution is separate from source-data rights.

## Known limitations and owner blockers

1. **No generic authenticated HTTP/IK ingress profile**; the existing build profile has restricted sender semantics.
2. **No adopted DaaT↔Médiathèque handoff**; preview file references are local and not source-custody receipts.
3. **No Framework v11 / diK / Kit authoring connector**, crosswalk approval or automatic KQ/KP/KA/KS identity creation.
4. **No real PhilPapers/Crossref/OpenAlex harvesting, Acomba SDK/ODBC or CDC**; source grants, rate restrictions, database consistency and data rights remain with the source host.
5. **No production-grade untrusted PDF sandbox**, OCR/model downloading, malware scanner, DLP, API secret vault, hosting service or durable **owner-effect** outbox. Use bounded, already approved files in an isolated environment only.
6. **No production security certification**: local tests alone do not prove trusted identity, Konfid transport, permissions, actual owner integration, parser sandboxing or runtime suitability.
7. **No automatic RO-Crate/PROV-O replacement schema**: Kristal owner profiles are reused where actually supported at a pinned revision.
8. The project license, copied owner contract redistribution and hosted third-party license audits remain owner decisions per `LICENSE-POLICY.md`.

## Implementation gate for future real integration

To enable live ingestion for a given family, require: owner-approved exact source disclosure permission; chosen and pinned adapter/worker + its OSS license and sandbox; host-authenticated workload and actor; Konfid-backed policy with audit; immutable source reference and ownership verifier; a reviewed DaaT mapping; applicable source-custody handoff; review in diK/Kristalizer and explicit Framework/Kit interface; independent bilateral qualification before a production claim. Do not use `kristal.build.request/2.0.0` as a generic upload command.

## Testing and qualification

Run one consolidated final test suite once code and fixtures are complete (see `tests/test_onramp_*.py`), retaining existing v0.3 tests. Distinguish **offline fixture test** from real source-owner acceptance and from independently qualified release. Tests must include no external API credentials or real accounting/medical data.
