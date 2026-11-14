"""Bounded, read-only owner preflight and noncanonical Kristal review handoff.

This is NOT an IK ingress profile, Authoring Kit importer, signed approval,
semantic KQ/KP/KA/KS minting, or permission to write a Kit workspace.
Owner repositories remain independently installed and authoritative.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
from typing import Any, Mapping

from .errors import AdmissionError
from .review import verify_review_packet
from .verification import verify_preparation
from .util import json_digest, load_json
from .owner_inventory import read_c0_owner_hints

_KIT_VERSION = '4.0.0-draft.4'
_FRAMEWORK_VERSION = '11.0.0-draft.4'
_PIN_PROFILE = 'kristal-integration-framework-pin/v11.0-draft.4'
_HANDOFF_FORMAT = 'daat.kristal-review-handoff/0.1.0-prototype'
_RE_SHA = re.compile(r'^[a-f0-9]{64}$')
_KNOWN = {
    'framework': ('Kristal-Framework', 'Kristal/Kristal-Framework'),
    'kit': ('Kristal-Authoring-Kit', 'Kristal/Kristal-Authoring-Kit'),
    'kristalizer': ('Kristalizer', 'Kristal/Kristalizer'),
    'dik': ('diK/diK', 'diK'),
    'arketype': ('Kristal/Arketype/arketype', 'Arketype/arketype', 'Arketype'),
}


def _safe_root(path: Path | str) -> Path:
    p = Path(path).expanduser()
    if not p.is_dir() or p.is_symlink():
        raise AdmissionError('OWNER_ROOT_INVALID', 'Owner path must be an existing, non-symlink directory')
    resolved = p.resolve()
    if resolved != p.absolute():
        # An explicit physical root must not traverse a junction/symlink to another checkout.
        raise AdmissionError('OWNER_ROOT_INVALID', 'Ambiguous owner root; use its physical absolute path')
    return resolved


def _read_small(path: Path, limit: int = 100_000) -> str:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > limit:
        raise AdmissionError('OWNER_SOURCE_INVALID', 'Missing, linked or oversized owner source metadata')
    return path.read_text(encoding='utf-8-sig')


def _file_sha(path: Path, *, limit: int = 4_000_000) -> str:
    if not path.is_file() or path.is_symlink() or path.stat().st_size > limit:
        raise AdmissionError('OWNER_SOURCE_INVALID', 'Missing, linked or oversized pinned owner source file')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(65536), b''):
            digest.update(part)
    return digest.hexdigest()


def _owner_file(root: Path, rel: str) -> Path:
    """Resolve only regular files from a pinned relative name below one root."""
    p = Path(rel)
    if p.is_absolute() or not p.parts or any(x in ('', '.', '..') for x in p.parts):
        raise AdmissionError('OWNER_PIN_INVALID', 'Owner pin contains an unsafe path')
    target = root
    for segment in p.parts:
        target = target / segment
        if target.is_symlink():
            raise AdmissionError('OWNER_PIN_INVALID', 'Owner pin traverses a symlink')
    if not target.resolve().is_relative_to(root):
        raise AdmissionError('OWNER_PIN_INVALID', 'Owner pin escapes root')
    return target


def discover_roots(base: Path | str, overrides: Mapping[str, Path | str] | None = None, *,
                   inventory: Path | str | None = None) -> dict[str, Path | None]:
    """Known explicit layout only; no recursive searching or silent fallback after overrides."""
    top = _safe_root(base)
    selected: dict[str, Path | None] = {}
    overrides = overrides or {}
    hints = read_c0_owner_hints(top, inventory)
    markers = {
        'framework': ('VERSION', 'schemas/v11/kristal-semantic-graph.schema.json'),
        'kit': ('VERSION', 'tools/kristal.py'),
        'kristalizer': ('VERSION', 'kristalizer.py'),
        'dik': ('spec/diK-1.0/AGENTS.md',),
        'arketype': ('AGENTS.md',),
    }
    for name, variants in _KNOWN.items():
        if name in overrides and overrides[name] is not None:
            selected[name] = _safe_root(overrides[name])
            continue
        if hints is not None and hints['paths_by_role'].get(name) is not None:
            # An inventory record is a location hint; no fallback to an unrelated
            # checkout if it is absent or fails the owner's identity markers.
            hint = hints['paths_by_role'][name]
            if not hint.is_dir() or not all((hint / marker).is_file() for marker in markers[name]):
                selected[name] = None
                continue
            selected[name] = _safe_root(hint)
            continue
        matches = [top / Path(x) for x in variants if (top / Path(x)).is_dir() and
                   all((top / Path(x) / f).is_file() for f in markers[name])]
        if len(matches) > 1:
            raise AdmissionError('OWNER_ROOT_AMBIGUOUS', f'More than one {name} owner root; specify explicit path')
        selected[name] = _safe_root(matches[0]) if matches else None
    roots = [str(p).casefold() for p in selected.values() if p is not None]
    if len(roots) != len(set(roots)):
        raise AdmissionError('OWNER_ROOT_AMBIGUOUS', 'Independent owner roles must not point at same directory')
    return selected


def dik_v11_schema_parity(framework: Path, dik: Path) -> dict[str, Any]:
    """Read-only, byte-exact parity check from Kit Branch02 checker semantics.

    Schema byte parity is NOT diK alpha.7 functional compatibility, semantic
    approval, a verified identity mapping, or permission to import a catalog.
    """
    result: dict[str, Any] = {
        'schema_byte_parity': False,
        'compared_schema_count': 0,
        'schema_drift': [],
        'parity_scope': 'schema_bytes_only_not_functional_qualification',
    }
    try:
        metadata = _read_small(_owner_file(dik, 'pyproject.toml'))
        if not re.search(r'(?m)^version\s*=\s*[\"\']1\.0\.0a7[\"\']\s*$', metadata):
            result['reason'] = 'unexpected_dik_version'
            return result
        framework_schema = _owner_file(framework, 'schemas/v11')
        dik_schema = _owner_file(dik, 'src/dik/_framework/schemas/v11')
        if not framework_schema.is_dir() or not dik_schema.is_dir():
            result['reason'] = 'v11_schema_directory_missing'
            return result
        ours = {p.name: p for p in framework_schema.glob('*.schema.json')}
        theirs = {p.name: p for p in dik_schema.glob('*.schema.json')}
        if len(ours) != 11 or ours.keys() != theirs.keys():
            result['reason'] = 'schema_inventory_mismatch'
            return result
        drift = []
        for name in sorted(ours):
            left = _file_sha(_owner_file(framework, 'schemas/v11/' + name))
            right = _file_sha(_owner_file(dik, 'src/dik/_framework/schemas/v11/' + name))
            if left != right:
                drift.append(name)
        result['compared_schema_count'] = len(ours)
        result['schema_drift'] = drift
        result['schema_byte_parity'] = not drift
        return result
    except (AdmissionError, OSError, UnicodeError):
        result['reason'] = 'source_unreadable_or_untrusted'
        return result


def owner_preflight(base: Path | str, *, overrides: Mapping[str, Path | str] | None = None,
                    inventory: Path | str | None = None) -> dict[str, Any]:
    """Read-only verification of actual owner source bytes against Kit's declared pin.

    An exact digest match is local consistency, not proof the pin's author or
    artifacts are authenticated. No external command or network access.
    """
    top = _safe_root(base)
    hints = read_c0_owner_hints(top, inventory)
    paths = discover_roots(top, overrides, inventory=inventory)
    components: dict[str, Any] = {}
    blockers: list[str] = []
    for name, path in paths.items():
        components[name] = {'present': path is not None, 'path': str(path) if path else None}
    kit, fw = paths['kit'], paths['framework']
    if kit is None or fw is None:
        blockers.append('framework_and_kit_must_be_installed_separately')
    else:
        try:
            if kit == fw or kit.is_relative_to(fw) or fw.is_relative_to(kit):
                raise AdmissionError('OWNER_ROOT_INVALID', 'Framework and Kit must be separate roots')
            version = _read_small(_owner_file(kit, 'VERSION')).strip()
            fw_version = _read_small(_owner_file(fw, 'VERSION')).strip()
            components['kit']['version'] = version
            components['framework']['version'] = fw_version
            if version != _KIT_VERSION:
                blockers.append('unapproved_kit_version')
            if fw_version != _FRAMEWORK_VERSION:
                blockers.append('unapproved_framework_version')
            from json import loads
            pin = loads(_read_small(_owner_file(kit, 'contracts/v11-framework-pin.json')))
            files = pin.get('files')
            if pin.get('profile') != _PIN_PROFILE or pin.get('version') != _FRAMEWORK_VERSION or not isinstance(files, dict) or len(files) < 13:
                raise AdmissionError('OWNER_PIN_INVALID', 'Kit pin does not match expected Framework draft.4 profile')
            required = {'VERSION', 'schemas/v11/kristal-semantic-graph.schema.json',
                        'schemas/v11/kristal-identity-registry.schema.json',
                        'schemas/v11/kristal-external-crosswalk.schema.json',
                        'schemas/v11/kristal-dictionary-catalog.schema.json'}
            if not required.issubset(files):
                raise AdmissionError('OWNER_PIN_INVALID', 'Kit pin missing critical v11 semantic contracts')
            drift: list[str] = []
            for rel, expected in sorted(files.items()):
                if not isinstance(expected, str) or not _RE_SHA.fullmatch(expected):
                    raise AdmissionError('OWNER_PIN_INVALID', 'Invalid Kit Framework pin digest')
                try:
                    observed = _file_sha(_owner_file(fw, rel))
                except AdmissionError:
                    drift.append(rel)
                    continue
                if observed != expected:
                    drift.append(rel)
            components['framework']['pinned_files_checked'] = len(files)
            components['framework']['pin_drift'] = drift
            components['kit']['pin_profile'] = pin['profile']
            if drift:
                blockers.append('framework_pin_mismatch')
            if not _owner_file(kit, 'tools/kristal.py').is_file():
                blockers.append('kit_cli_missing')
        except (ValueError, KeyError, TypeError, UnicodeError, AdmissionError) as exc:
            components['framework']['pin_error_code'] = getattr(exc, 'code', 'OWNER_PIN_INVALID')
            blockers.append('framework_pin_verification_failed')
    if paths['kristalizer'] is None:
        blockers.append('kristalizer_missing')
    else:
        try:
            components['kristalizer']['version'] = _read_small(_owner_file(paths['kristalizer'], 'VERSION')).strip()
            if not _owner_file(paths['kristalizer'], 'kristalizer.py').is_file():
                blockers.append('kristalizer_cli_missing')
        except AdmissionError:
            blockers.append('kristalizer_metadata_missing')
    if paths['dik'] is not None:
        components['dik']['compatibility'] = 'requires_explicit_draft3_to_draft4_functional_qualification'
        if paths['framework'] is not None:
            parity = dik_v11_schema_parity(paths['framework'], paths['dik'])
            components['dik'].update(parity)
            if not parity['schema_byte_parity']:
                blockers.append('dik_v11_schema_parity_not_verified')
        blockers.append('dik_draft_compatibility_not_qualified')
    if paths['arketype'] is not None:
        components['arketype']['role'] = 'non_normative_design_hints_only'
    if paths['dik'] is None:
        blockers.append('dik_not_installed_or_not_explicitly_selected')
    if paths['arketype'] is None:
        blockers.append('arketype_not_installed_or_not_explicitly_selected')
    # This status never asserts actual inter-repository authoring qualification.
    return {
        'format': 'daat.kristal-owner-preflight/0.2.0-prototype',
        'inventory': ({'relative_path': hints['inventory_relative_path'],
                       'sha256': hints['inventory_sha256'],
                       'authority_granted': False} if hints else None),
        'status': 'local_source_pin_checked' if not blockers else 'blocked',
        'checks': components, 'blockers': sorted(set(blockers)),
        'draft_compatibility': 'unqualified_dik_draft3_vs_kit_framework_draft4',
        'owner_effects_authorized': False,
        'semantic_approval': False,
        'ik_ingress_approved': False,
        'publication_authorized': False,
        'verification_level': 'local_file_integrity_only_not_bilateral_tck',
    }


def prepare_handoff(preview: dict[str, Any], review: dict[str, Any], *,
                    include_evidence: bool = False) -> dict[str, Any]:
    """Package a cryptographically bound *local proposal* for owner consideration.

    Never writes canonical Kristals. A user's review name is an assertion,
    not verified identity; exact Kit admission must be handled by its owner.
    """
    verify_preparation(preview)
    verify_review_packet(review)
    if review.get('preview_sha256') != preview['preview_sha256'] or review.get('source_manifest_sha256') != preview['source']['manifest_sha256']:
        raise AdmissionError('HANDOFF_PREVIEW_MISMATCH', 'Review and preview do not refer to same exact source')
    candidates = {c['candidate_id']: c for c in preview.get('candidates', [])}
    records = {r['local_evidence_id']: r for r in preview['records']}
    reviewed: dict[str, Any] = {}
    for entry in review['decisions']:
        if not isinstance(entry, dict):
            raise AdmissionError('HANDOFF_REVIEW_INVALID', 'Bad decision record')
        ident = entry.get('candidate_id')
        if ident not in candidates or ident in reviewed or entry.get('evidence_id') != candidates[ident]['evidence_id']:
            raise AdmissionError('HANDOFF_REVIEW_INVALID', 'Review references unknown/duplicate or mismatched candidate')
        if entry.get('decision') not in ('reject', 'defer', 'submit_to_owner'):
            raise AdmissionError('HANDOFF_REVIEW_INVALID', 'Unsupported review decision')
        reviewed[ident] = entry
    if set(review.get('unreviewed_candidate_ids', [])) != set(candidates) - set(reviewed):
        raise AdmissionError('HANDOFF_REVIEW_INVALID', 'Unreviewed candidates are not accounted for')
    offered = []
    for ident in sorted(reviewed):
        decision = reviewed[ident]
        if decision['decision'] != 'submit_to_owner':
            continue
        candidate = candidates[ident]
        record = records.get(candidate['evidence_id'])
        if record is None or record.get('source_sha256') != candidate.get('source_sha256'):
            raise AdmissionError('HANDOFF_EVIDENCE_INVALID', 'Missing or inconsistent candidate evidence')
        item = {
            'candidate_id': ident,
            'evidence_id': candidate['evidence_id'],
            'source_anchor': record['anchor'],
            'source_sha256': record['source_sha256'],
            'record_type': record['record_type'],
            'proposed_arketypes': candidate['proposed_arketypes'],
            'external_identifiers_unreviewed': candidate.get('external_identifiers_unreviewed', {}),
            'review_reason': decision['reason'],
            'semantic_identity': None,
        }
        if include_evidence:
            item['source_record_data_unverified'] = record['data']
        offered.append(item)
    packet = {
        'format': _HANDOFF_FORMAT,
        'state': 'offline_noncanonical_review_transfer_not_approved_ingress',
        'source': preview['source'],
        'preview_sha256': preview['preview_sha256'],
        'review_sha256': review['packet_sha256'],
        'reviewer_assertion_unverified': review['reviewer_assertion'],
        'purpose': review['purpose'],
        'submitted_candidates': offered,
        'submitted_count': len(offered),
        'unreviewed_count': len(review['unreviewed_candidate_ids']),
        'rejected_or_deferred_count': len(review['decisions']) - len(offered),
        'source_data_copied': bool(include_evidence),
        'recipient_roles': ['Kristalizer (review proposal)', 'diK (lexical/crosswalk proposals)',
                            'Kristal Authoring Kit (separate approved admission)'],
        'prohibited_effects': ['mint_KQ_KP_KA_KS', 'activate', 'publish', 'write_owner_workspace'],
        'required_admissions': ['source_custody_permission', 'authenticated_reviewer',
                                'reviewed_semantic_mapping', 'owner_adopted_versioned_contract',
                                'exact_framework_and_kit_pins', 'receiving_owner_validation'],
        'owner_contract': None, 'owner_approval': None,
        'ik_ingress_approved': False, 'publication_authorized': False,
    }
    packet['handoff_sha256'] = json_digest(packet)
    return packet


def verify_handoff(packet: dict[str, Any], *, preview: dict[str, Any] | None = None,
                   review: dict[str, Any] | None = None) -> dict[str, Any]:
    """Verify local packet structure/hash and optionally exact source references.

    Hashes are not signatures, attestations of semantic truth or owners' acceptance.
    """
    if not isinstance(packet, dict) or packet.get('format') != _HANDOFF_FORMAT:
        raise AdmissionError('HANDOFF_INVALID', 'Unknown Kristal handoff prototype format')
    expected_keys = {
        'format', 'state', 'source', 'preview_sha256', 'review_sha256',
        'reviewer_assertion_unverified', 'purpose', 'submitted_candidates',
        'submitted_count', 'unreviewed_count', 'rejected_or_deferred_count',
        'source_data_copied', 'recipient_roles', 'prohibited_effects',
        'required_admissions', 'owner_contract', 'owner_approval',
        'ik_ingress_approved', 'publication_authorized', 'handoff_sha256',
    }
    if set(packet) != expected_keys:
        raise AdmissionError('HANDOFF_INVALID', 'Undeclared fields in local handoff packet')
    if type(packet['source_data_copied']) is not bool:
        raise AdmissionError('HANDOFF_INVALID', 'Raw source flag must be boolean')
    for field in ('submitted_count', 'unreviewed_count', 'rejected_or_deferred_count'):
        if type(packet[field]) is not int or packet[field] < 0:
            raise AdmissionError('HANDOFF_INVALID', 'Counts must be nonnegative integers')
    if packet.get('prohibited_effects') != ['mint_KQ_KP_KA_KS', 'activate', 'publish', 'write_owner_workspace']:
        raise AdmissionError('HANDOFF_AUTHORITY_INVALID', 'Local handoff must explicitly forbid owner effects')
    if packet.get('required_admissions') != ['source_custody_permission', 'authenticated_reviewer',
                                              'reviewed_semantic_mapping', 'owner_adopted_versioned_contract',
                                              'exact_framework_and_kit_pins', 'receiving_owner_validation']:
        raise AdmissionError('HANDOFF_AUTHORITY_INVALID', 'Mandatory receiving owner gates missing')
    if packet.get('recipient_roles') != ['Kristalizer (review proposal)', 'diK (lexical/crosswalk proposals)',
                                         'Kristal Authoring Kit (separate approved admission)']:
        raise AdmissionError('HANDOFF_INVALID', 'Incorrect proposed reviewer roles')
    if not isinstance(packet['source'], dict) or not isinstance(packet.get('preview_sha256'), str) or not _RE_SHA.fullmatch(packet['preview_sha256']):
        raise AdmissionError('HANDOFF_INVALID', 'Malformed source reference or preview digest')
    if not isinstance(packet.get('review_sha256'), str) or not _RE_SHA.fullmatch(packet['review_sha256']):
        raise AdmissionError('HANDOFF_INVALID', 'Missing review digest')
    if not isinstance(packet['reviewer_assertion_unverified'], str) or not packet['reviewer_assertion_unverified']:
        raise AdmissionError('HANDOFF_INVALID', 'Missing reviewer reference')

    if (packet.get('state') != 'offline_noncanonical_review_transfer_not_approved_ingress'
            or packet.get('owner_contract') is not None or packet.get('owner_approval') is not None
            or packet.get('publication_authorized') is not False
            or packet.get('ik_ingress_approved') is not False):
        raise AdmissionError('HANDOFF_AUTHORITY_INVALID', 'Prototype cannot assert owner authority')
    observed = packet.get('handoff_sha256')
    body = dict(packet)
    body.pop('handoff_sha256', None)
    if not isinstance(observed, str) or not _RE_SHA.fullmatch(observed) or json_digest(body) != observed:
        raise AdmissionError('HANDOFF_INTEGRITY', 'Handoff content does not match SHA-256')
    items = packet.get('submitted_candidates')
    if not isinstance(items, list) or len(items) != packet.get('submitted_count'):
        raise AdmissionError('HANDOFF_INVALID', 'Handoff count mismatch')
    ids: set[str] = set()
    for item in items:
        expected_item_keys = {'candidate_id', 'evidence_id', 'source_anchor', 'source_sha256',
                              'record_type', 'proposed_arketypes', 'external_identifiers_unreviewed',
                              'review_reason', 'semantic_identity'}
        if packet['source_data_copied']:
            expected_item_keys.add('source_record_data_unverified')
        if not isinstance(item, dict) or set(item) != expected_item_keys or item.get('semantic_identity') is not None:
            raise AdmissionError('HANDOFF_AUTHORITY_INVALID', 'Handoff attempted undeclared or canonical fields')
        if not isinstance(item.get('source_anchor'), dict) or not isinstance(item.get('proposed_arketypes'), list):
            raise AdmissionError('HANDOFF_INVALID', 'Invalid evidence anchor or design hints')
        if not isinstance(item.get('evidence_id'), str) or not isinstance(item.get('candidate_id'), str) or not _RE_SHA.fullmatch(item.get('source_sha256', '')):
            raise AdmissionError('HANDOFF_INVALID', 'Unbound candidate evidence in handoff')
        if item['candidate_id'] in ids:
            raise AdmissionError('HANDOFF_INVALID', 'Duplicate candidate in handoff')
        ids.add(item['candidate_id'])
        if ('source_record_data_unverified' in item) != (packet.get('source_data_copied') is True):
            raise AdmissionError('HANDOFF_INVALID', 'Raw source inclusion declaration mismatch')
    if preview is not None and review is not None:
        reference = prepare_handoff(preview, review, include_evidence=packet['source_data_copied'])
        if reference != packet:
            raise AdmissionError('HANDOFF_PREVIEW_MISMATCH', 'Handoff differs from exact source review')
    return {'valid': True, 'handoff_sha256': observed, 'submitted_count': len(items),
            'source_data_copied': packet['source_data_copied'],
            'authority': 'none_local_preview_only'}
