"""Source release file integrity manifest (not a digital signature)."""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'REPOSITORY-MANIFEST.json'
EXCLUDE_DIRS={'.git','__pycache__','.pytest_cache','.venv','build','dist','out','.tmp-install'}

def collect():
    result={}
    for p in sorted(ROOT.rglob('*')):
        if p.is_symlink():raise ValueError(f'Symlink forbidden in release: {p.relative_to(ROOT)}')
        if not p.is_file() or any(part in EXCLUDE_DIRS or part.endswith('.egg-info') for part in p.relative_to(ROOT).parts):continue
        if p==MANIFEST or p.suffix in ('.pyc','.pyo'):continue
        result[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    return {'algorithm':'sha256','files':result}

def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args(argv)
    expected=collect()
    if args.write:
        MANIFEST.write_text(json.dumps(expected,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
        print('Wrote source manifest:',len(expected['files']),'files');return 0
    if not MANIFEST.is_file() or json.loads(MANIFEST.read_text())!=expected:
        print('Source manifest mismatch; see REPOSITORY-MANIFEST.json',file=sys.stderr);return 1
    print('Source manifest verified:',len(expected['files']),'files');return 0

if __name__=='__main__':sys.exit(main())
