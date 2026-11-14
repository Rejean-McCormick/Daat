"""Read-only interpretation of kOA C0's declared local repository paths.

The C0 inventory is a *location hint*, NOT a trust anchor, source grant or
an owner contract. Do not follow arbitrary paths supplied by the inventory;
normalize only C:\\mycode\\... entries under an explicitly selected local
checkout root. Owner pins and independently approved admissions still apply.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PureWindowsPath
from typing import Any

from .errors import AdmissionError

# Repository IDs come from kOA's docs/inventory/repositories.json. They are
# location hints, not imported authorities or new runtime dependencies.
_REPOS = {
    'framework': 'Kristal-Framework',
    'kit': 'Kristal-Authoring-Kit',
    'kristalizer': 'Kristalizer',
    'dik': 'diK',
    'arketype': 'Arketype',
    'interaction_kernel': 'Interaction-Kernel',
    'skope': 'Skope',
    'mediatheque': 'Mediatheque',
    'mediatheque_blank': 'Mediatheque-blank',
    'konfid': 'Konfid',
    'integration_pack': 'Kristal-Integration-Pack',
    'manager': 'Kristal-Manager',
    'daat': 'Daat',
    'koa': 'kOA-Digital-Ecosystem',
}

# Only an exact, bounded, local inventory location is auto-detected.
_DEFAULT_INVENTORY = Path('kOA_Digital_Ecosystem/kOA_Digital_Ecosystem/docs/inventory/repositories.json')


def _inventory_file(root: Path, selected: Path | str | None) -> Path | None:
    if selected is None:
        path = root / _DEFAULT_INVENTORY
        if not path.exists():
            return None
    else:
        path = Path(selected).expanduser()
        if not path.is_absolute():
            path = root / path
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
        raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 inventory must be a regular file inside selected root')
    probe = root
    for part in path.relative_to(root).parts:
        probe = probe / part
        if probe.is_symlink():
            raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 inventory path traverses a symbolic link')
    if path.stat().st_size > 1_000_000:
        raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 inventory exceeds byte limit')
    return path


def read_c0_owner_hints(root: Path, selected: Path | str | None = None) -> dict[str, Any] | None:
    """Resolve source-location hints without reading owner content or executing code.

    Only C:\\mycode\\... coordinates may be relocated under ``root``. A
    malicious/malformed entry is refused; this function does not grant access
    to any source, translate tenant rights or verify a signature.
    """
    path = _inventory_file(root, selected)
    if path is None:
        return None
    raw = path.read_bytes()
    try:
        items = json.loads(raw.decode('utf-8-sig'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 inventory JSON invalid') from exc
    if not isinstance(items, list) or len(items) > 200:
        raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 inventory must contain a bounded repository list')
    by_repo: dict[str, Path] = {}
    expected = set(_REPOS.values())
    for record in items:
        if not isinstance(record, dict):
            raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 inventory has a non-object row')
        repo_id = record.get('github_repo')
        if not isinstance(repo_id, str) or not repo_id.startswith('Rejean-McCormick/'):
            continue
        name = repo_id.partition('/')[2]
        if name not in expected:
            continue
        if name in by_repo:
            raise AdmissionError('OWNER_INVENTORY_INVALID', 'Duplicate owner identity in C0 inventory')
        windows = record.get('local_root')
        if not isinstance(windows, str):
            raise AdmissionError('OWNER_INVENTORY_INVALID', 'Missing local_root in C0 owner entry')
        p = PureWindowsPath(windows)
        # Reject alternate drives, UNC, dot segments and arbitrary host roots.
        if (not p.is_absolute() or len(p.parts) < 4 or
                p.parts[0].casefold() != 'c:\\' or p.parts[1].casefold() != 'mycode' or
                any(part in ('.', '..', '') for part in p.parts[2:])):
            raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 owner path is outside documented C:\\mycode tree')
        relative = Path(*p.parts[2:])
        mapped = root / relative
        if not mapped.resolve().is_relative_to(root):
            raise AdmissionError('OWNER_INVENTORY_INVALID', 'C0 owner path escapes selected root')
        by_repo[name] = mapped
    return {
        'format': 'daat.c0-owner-location-hints/0.1.0-local',
        'inventory_relative_path': path.relative_to(root).as_posix(),
        'inventory_sha256': hashlib.sha256(raw).hexdigest(),
        'paths_by_role': {role: by_repo.get(repo) for role, repo in _REPOS.items()},
        'status': 'untrusted_location_hints_only',
        'owner_authority_granted': False,
    }
