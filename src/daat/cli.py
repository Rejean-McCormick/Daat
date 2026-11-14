"""Offline-only CLI. No network listener, implicit credentials or canonical writes."""
from __future__ import annotations
import argparse
import json
import sqlite3
import sys
from pathlib import Path
from .contracts import verify_baseline, validate_owner, verify_payload_profile
from .alignment import evaluate
from .mapping import load_profile, map_file
from .util import load_json, write_json, json_digest, file_digest
from .errors import DaatError


def _source_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, required=True, help="Explicit selected local source root")
    parser.add_argument("--source", required=True, help="Path relative to selected root; never a URL")
    parser.add_argument("--kind", choices=["pdf", "git", "archive", "dataset", "bibliography", "acomba"], required=True)
    parser.add_argument("--family", required=True, help="Two-digit ID from source catalogue")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--license", required=True, help="Source license or terms declaration")
    parser.add_argument("--rights-acknowledged", action="store_true", help="Explicit local rights acknowledgement (NOT verified external grant)")
    parser.add_argument("--classification", choices=["public", "internal", "confidential", "restricted"], default="internal")
    parser.add_argument("--redistributable", action="store_true")
    parser.add_argument("--valid-until", default=None, help="Expiry ISO timestamp with UTC offset")
    parser.add_argument("--commit", help="Full immutable Git commit SHA; mandatory for kind=git")
    parser.add_argument("--record-type", help="Typed accounting entity, required for kind=acomba")
    parser.add_argument("--mode", choices=["snapshot", "reference"], default="snapshot")
    parser.add_argument("--max-bytes", type=int, default=20_000_000)
    parser.add_argument("--max-records", type=int, default=500)


def _selection(args: argparse.Namespace):
    from .source import SourceSelection, RightsDeclaration, ReadLimits
    grant = RightsDeclaration(
        tenant=args.tenant, purpose=args.purpose, license=args.license,
        asserted_by=args.actor, permission_asserted=args.rights_acknowledged,
        classification=args.classification, redistributable=args.redistributable,
        valid_until=args.valid_until,
    )
    limits = ReadLimits(max_source_bytes=args.max_bytes, max_records=args.max_records)
    return SourceSelection(args.root, args.source, args.kind, args.family, grant,
                           mode=args.mode, record_type=args.record_type,
                           revision=args.commit, limits=limits)


def _prepare_cli(args: argparse.Namespace) -> dict:
    from .pipeline import prepare_local, concise_report
    from .output import write_private_json
    from .journal import LocalPreviewJournal
    from .registry import builtin_registry
    from .source import bounded_file_digest
    source = _selection(args)
    # Validate family/adapter and file path before any read.
    builtin_registry().resolve(source)
    path = source.path()
    if args.journal is not None and (args.out is None or not args.intent_key):
        raise DaatError("JOURNAL_INVALID", "Journal requires --out and --intent-key")
    journal = LocalPreviewJournal(args.journal) if args.journal is not None else None
    intent = None
    try:
        if journal is not None:
            # Digest source bytes for files; pin immutable commit for local Git.
            sha = source.revision if source.kind == "git" else bounded_file_digest(path, max_bytes=source.limits.max_source_bytes)
            profile_sha = file_digest(args.mapping_profile) if args.mapping_profile else None
            intent = json_digest({"kind": source.kind, "family": source.family_id,
                                  "root": str(source.root.resolve()), "source": source.relative_path,
                                  "mode": source.mode, "record_type": source.record_type,
                                  "source_pin": sha, "mapping_sha256": profile_sha,
                                  "rights": source.rights.public_metadata(), "limits": vars(source.limits)})
            entry = journal.begin(args.intent_key, intent)
            if not entry.newly_created:
                raise DaatError("JOURNAL_RECONCILE", "Existing intent: inspect journal; no blind retry")
        prepared = prepare_local(source, mapping_profile=args.mapping_profile, candidates=not args.no_candidates)
        if args.out is not None:
            write_private_json(args.out, prepared, replace=args.replace)
        if journal is not None and intent is not None:
            journal.terminal(args.intent_key, intent, state="finished", output_sha256=prepared["preview_sha256"])
        summary = concise_report(prepared)
        if args.out is None:
            summary["note"] = "No source content printed or persisted; --out writes a private local JSON preview"
        else:
            summary["output_written"] = True
        return summary
    except BaseException:
        if journal is not None and intent is not None:
            # Cannot always know whether output replace succeeded; require explicit reconciliation.
            try:
                entry = journal.inspect(args.intent_key)
                if entry and entry.state == "running":
                    journal.terminal(args.intent_key, intent, state="uncertain")
            except Exception:
                pass
        raise
    finally:
        if journal is not None:
            journal.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="daat", description="DaaT offline source prep and IK v6 contract toolkit (not a deployed service)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify-contracts", help="Verify pinned owner contracts and v6 lock")
    vm = sub.add_parser("validate-mapping"); vm.add_argument("profile", type=Path)
    mm = sub.add_parser("map"); mm.add_argument("profile", type=Path); mm.add_argument("input", type=Path); mm.add_argument("--out", type=Path)
    am = sub.add_parser("alignment-report"); am.add_argument("profile", type=Path); am.add_argument("--out", type=Path)
    vi = sub.add_parser("validate-ik"); vi.add_argument("kind", choices=["envelope", "receipt", "artifact-ref", "export-manifest", "build", "ready"]); vi.add_argument("input", type=Path)
    vb = sub.add_parser("validate-build"); vb.add_argument("input", type=Path)

    sub.add_parser("list-source-families", help="Print 36 research families (not available source connectors)")
    sub.add_parser("list-adapters", help="Print built-in offline read-only readers")
    diagnose = sub.add_parser("diagnose-local", help="Suggest source kind/lane/families without semantic inference")
    diagnose.add_argument("--root", type=Path, required=True)
    diagnose.add_argument("--source", required=True)
    diagnose.add_argument("--tenant", required=True)
    diagnose.add_argument("--actor", required=True)
    diagnose.add_argument("--purpose", required=True)
    diagnose.add_argument("--license", required=True)
    diagnose.add_argument("--rights-acknowledged", action="store_true")
    va = sub.add_parser("validate-adapter"); va.add_argument("manifest", type=Path)
    verify = sub.add_parser("verify-local-preview"); verify.add_argument("input", type=Path)
    prepare = sub.add_parser("prepare-local", help="Produce noncanonical local evidence and candidates, no owner writes")
    _source_options(prepare)
    prepare.add_argument("--mapping-profile", type=Path, help="Optional explicit local draft mapping profile")
    prepare.add_argument("--no-candidates", action="store_true")
    prepare.add_argument("--out", type=Path, help="Private local JSON preview; stdout remains summary-only")
    prepare.add_argument("--replace", action="store_true", help="Allow replacement of existing preview file")
    prepare.add_argument("--journal", type=Path, help="Optional local SQLite *preview-only* intent journal")
    prepare.add_argument("--intent-key", help="Operator idempotency key for a journaled local preview")
    review = sub.add_parser("prepare-review", help="Local review packet, never authoring approval")
    review.add_argument("preview", type=Path)
    review.add_argument("decisions", type=Path, help="JSON array of candidate_id/decision/reason")
    review.add_argument("--reviewer", required=True)
    review.add_argument("--purpose", required=True)
    review.add_argument("--out", type=Path, required=True)
    review.add_argument("--replace", action="store_true")
    verify_review = sub.add_parser("verify-review"); verify_review.add_argument("input", type=Path)
    inspect = sub.add_parser("inspect-journal"); inspect.add_argument("path", type=Path); inspect.add_argument("key")
    locations = sub.add_parser("kristal-owner-locations", help="Read declared checkout locations from kOA C0 inventory; no owner invocation")
    locations.add_argument("--root", type=Path, required=True, help="Actual local kOA workspace root, e.g. C:\\mycode")
    locations.add_argument("--inventory", type=Path, help="Optional explicit inventory path within the selected root")
    owner = sub.add_parser("kristal-owner-preflight", help="Read-only Framework/Kit/Kristalizer owner pin inspection; no owner invocation")
    owner.add_argument("--root", type=Path, required=True, help="Common local source-repository root, e.g. C:\\mycode")
    for name in ("framework", "kit", "kristalizer", "dik", "arketype"):
        owner.add_argument("--" + name, type=Path, help="Explicit root override (no implicit download)")
    owner.add_argument("--inventory", type=Path, help="Optional explicit kOA C0 repository inventory under --root")
    owner.add_argument("--out", type=Path, help="Private report output (optional)")
    handoff = sub.add_parser("kristal-prepare-handoff", help="Prepare noncanonical, offline reviewed candidate transfer (no owner import)")
    handoff.add_argument("--preview", type=Path, required=True)
    handoff.add_argument("--review", type=Path, required=True)
    handoff.add_argument("--out", type=Path, required=True)
    handoff.add_argument("--include-evidence", action="store_true", help="Explicitly include source records; keep resulting file private")
    handoff.add_argument("--replace", action="store_true")
    vh = sub.add_parser("kristal-verify-handoff", help="Check local handoff integrity and exact preview/review references")
    vh.add_argument("--handoff", type=Path, required=True)
    vh.add_argument("--preview", type=Path, help="Original preview (must be paired with --review)")
    vh.add_argument("--review", type=Path, help="Original review (must be paired with --preview)")
    audit = sub.add_parser("kristal-local-chain-audit", help="Verify exact offline preview/review/handoff binding (no owner writes)")
    audit.add_argument("--preview", type=Path, required=True)
    audit.add_argument("--review", type=Path, required=True)
    audit.add_argument("--handoff", type=Path, required=True)
    audit.add_argument("--root", type=Path, help="Optional local owner workspace for read-only pin inspection")
    audit.add_argument("--inventory", type=Path, help="Optional C0 inventory (requires --root)")
    audit.add_argument("--out", type=Path, help="Optional private audit JSON file")
    args = parser.parse_args(argv)
    try:
        result: dict | list | None = None
        if args.command == "verify-contracts": result = verify_baseline()
        elif args.command == "validate-mapping":
            p, _, _ = load_profile(args.profile)
            result = {"profile": p["id"] + "/" + p["version"], "status": "valid", "implementation_status": "local draft mapping format"}
        elif args.command == "map": result = map_file(args.profile, args.input)
        elif args.command == "alignment-report": result = evaluate(args.profile)
        elif args.command == "validate-ik":
            validate_owner(args.kind, load_json(args.input)); result = {"valid": True, "owner_schema": args.kind}
        elif args.command == "validate-build":
            verify_payload_profile(load_json(args.input)); result = {"valid": True, "IK_profile": "kristal.build.request/2.0.0"}
        elif args.command == "list-source-families":
            from .catalog import source_families
            result = [s.to_dict() for s in source_families()]
        elif args.command == "list-adapters":
            from .registry import builtin_registry
            result = builtin_registry().list()
        elif args.command == "diagnose-local":
            from .source import RightsDeclaration
            from .diagnosis import diagnose_local
            rights = RightsDeclaration(args.tenant, args.purpose, args.license, args.actor,
                                       args.rights_acknowledged)
            result = diagnose_local(args.root, args.source, rights)
        elif args.command == "validate-adapter":
            from .registry import read_adapter_manifest
            item = read_adapter_manifest(args.manifest)
            result = {"valid": True, "id": item["id"], "version": item["version"],
                      "meaning": "metadata_only_no_import_or_approved_host"}
        elif args.command == "prepare-local":
            result = _prepare_cli(args)
        elif args.command == "verify-local-preview":
            from .verification import verify_preparation
            result = verify_preparation(load_json(args.input, max_bytes=100_000_000))
        elif args.command == "prepare-review":
            from .review import prepare_review_packet
            from .output import write_private_json
            packet = prepare_review_packet(load_json(args.preview, max_bytes=100_000_000),
                                            load_json(args.decisions, max_bytes=2_000_000),
                                            reviewer=args.reviewer, purpose=args.purpose)
            write_private_json(args.out, packet, replace=args.replace)
            result = {"written": True, "packet_sha256": packet["packet_sha256"],
                      "authority": packet["state"], "reviewed": len(packet["decisions"])}
        elif args.command == "verify-review":
            from .review import verify_review_packet
            result = verify_review_packet(load_json(args.input, max_bytes=20_000_000))
        elif args.command == "inspect-journal":
            from .journal import LocalPreviewJournal
            with LocalPreviewJournal(args.path) as journal:
                entry = journal.inspect(args.key)
            result = vars(entry) if entry is not None else {"found": False}
        elif args.command == "kristal-owner-locations":
            from .owner_inventory import read_c0_owner_hints
            from .kristal_chain import _safe_root
            hints = read_c0_owner_hints(_safe_root(args.root), args.inventory)
            if hints is None:
                raise DaatError("OWNER_INVENTORY_MISSING", "No kOA C0 repository inventory at the documented relative location")
            result = {name: str(path) if path is not None else None
                      for name, path in hints["paths_by_role"].items()}
            result = {"inventory_sha256": hints["inventory_sha256"],
                      "inventory_relative_path": hints["inventory_relative_path"],
                      "status": "untrusted_location_hints_only", "owner_authority_granted": False,
                      "paths_by_role": result}
        elif args.command == "kristal-owner-preflight":
            from .kristal_chain import owner_preflight
            from .output import write_private_json
            overrides = {name: getattr(args, name) for name in ("framework", "kit", "kristalizer", "dik", "arketype")
                         if getattr(args, name) is not None}
            result = owner_preflight(args.root, overrides=overrides, inventory=args.inventory)
            if args.out:
                write_private_json(args.out, result)
                result = {"written": True, "status": result["status"], "blockers": result["blockers"],
                          "owner_effects_authorized": False}
        elif args.command == "kristal-prepare-handoff":
            from .kristal_chain import prepare_handoff
            from .output import write_private_json
            packet = prepare_handoff(load_json(args.preview, max_bytes=100_000_000),
                                     load_json(args.review, max_bytes=20_000_000),
                                     include_evidence=args.include_evidence)
            write_private_json(args.out, packet, replace=args.replace)
            result = {"written": True, "handoff_sha256": packet["handoff_sha256"],
                      "submitted_count": packet["submitted_count"], "source_data_copied": packet["source_data_copied"],
                      "authority": "none_local_preview_only"}
        elif args.command == "kristal-verify-handoff":
            from .kristal_chain import verify_handoff
            if (args.preview is None) != (args.review is None):
                raise DaatError("HANDOFF_INPUT_INVALID", "Provide both --preview and --review or neither")
            result = verify_handoff(load_json(args.handoff, max_bytes=100_000_000),
                                    preview=load_json(args.preview, max_bytes=100_000_000) if args.preview else None,
                                    review=load_json(args.review, max_bytes=20_000_000) if args.review else None)
        elif args.command == "kristal-local-chain-audit":
            from .chain_audit import audit_local_chain
            from .output import write_private_json
            if args.inventory is not None and args.root is None:
                raise DaatError("CHAIN_AUDIT_INPUT_INVALID", "--inventory requires --root")
            report = audit_local_chain(
                load_json(args.preview, max_bytes=100_000_000),
                load_json(args.review, max_bytes=20_000_000),
                load_json(args.handoff, max_bytes=100_000_000),
                owner_root=args.root, inventory=args.inventory)
            if args.out:
                write_private_json(args.out, report)
                result = {"written": True, "audit_sha256": report["audit_sha256"],
                          "status": report["status"], "owner_admission": "not_qualified"}
            else:
                result = report
        if getattr(args, "out", None) is not None and args.command in ("map", "alignment-report"):
            write_json(args.out, result)
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    except (DaatError, ValueError, TypeError, KeyError, OSError, sqlite3.Error) as exc:
        print(json.dumps({"ok": False, "code": getattr(exc, "code", "INPUT_ERROR"),
                          "error": str(exc) if isinstance(exc, DaatError) else "Local operation failed"},
                         ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
