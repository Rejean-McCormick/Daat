"""Offline self-check for DaaT information bridge TARGET documentation only.

This script does not authorize acquisition, contact external providers, or execute connectors.
Run from repo root: python docs/pont-information/validate_spec.py
"""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read_csv(name):
    with (HERE / 'data' / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main():
    registry = json.loads((ROOT / 'docs/data/platform-access-registry.v1.json').read_text(encoding='utf-8'))
    profiles = registry['platforms']
    families = registry['families']
    assert len(profiles) == 89, f'expected documented snapshot baseline 89, found {len(profiles)}'
    assert len(families) == 36, f'expected documented snapshot baseline 36, found {len(families)}'
    pids = [p['id'] for p in profiles]
    fids = [f['id'] for f in families]
    assert len(set(pids)) == len(pids) and len(set(fids)) == len(fids)
    assert all(p['daat_connector_status'] == 'not_certified' for p in profiles), 'do not upgrade catalogue status silently'
    assert sum(p['platform_doc_status'] == 'official_docs_checked' for p in profiles) == 14
    assert all(set(p['family_ids']).issubset(fids) for p in profiles)
    coverage = read_csv('plateformes-89-couverture.csv')
    assert len(coverage) == 89 and {row['profile_id'] for row in coverage} == set(pids)
    assert all(row['daat_connector_status'] == 'not_certified' for row in coverage)
    tasks = read_csv('travaux-livraison-unique.csv')
    assert len(tasks) == 160 and len({r['task_id'] for r in tasks}) == 160
    assert {r['workstream'] for r in tasks} == {f'W{i:02d}' for i in range(1, 21)}
    assert all(r['status_at_specification'] == 'PROPOSED_NOT_IMPLEMENTED' for r in tasks)
    cases = read_csv('cas-tests-acceptation.csv')
    assert len(cases) == 674 and len({r['test_id'] for r in cases}) == len(cases)
    assert all(r['status_at_specification'] == 'DESIGNED_NOT_RUN' for r in cases)
    from jsonschema import Draft202012Validator
    schema = json.loads((HERE/'schemas/context-bundle.example.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    bundle = json.loads((HERE/'examples/context-bundle.example.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema).validate(bundle)
    sources = {s['source_ref']: s for s in bundle['sources']}
    frags = {f['fragment_id']: f for f in bundle['fragments']}
    assert len(frags) == len(bundle['fragments'])
    for f in bundle['fragments']:
        src = sources[f['source_ref']]
        assert src['rights']['ai_disclosure'] == 'allowed', 'never include unauthorized text'
        assert src['revision'] == f['source_revision']
        assert f['sha256'] == hashlib.sha256(f['text'].encode('utf-8')).hexdigest()
    assert set(bundle['disclosure']['permitted_fragment_ids']) == set(frags)
    assert bundle['disclosure']['status'] == 'prepared_not_sent'
    assert not any('kristal_state' in str(x) for x in bundle['fragments'])
    docs = sorted(HERE.glob('[0-9][0-9]-*.md'))
    assert len(docs) == 21, f'21 documentation chapters expected, found {len(docs)}'
    assert (ROOT/'docs/decisions/ADR-0005-DAAT-INFORMATION-BRIDGE-CHATGPT-CONTEXT.md').is_file()
    print('DaaT bridge documentation validation PASS')
    print(f'Profiles: {len(profiles)}; families: {len(families)}; tasks: {len(tasks)}; test cases designed: {len(cases)}')
    print(f'Chapters: {len(docs)}, example JSON Schema/rights/hashes valid; 0 providers promoted to operational')
    return 0


if __name__ == '__main__':
    sys.exit(main())
