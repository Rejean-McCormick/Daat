#!/usr/bin/env python3
"""Consultation locale du registre d'accès des plateformes DaAT, sans réseau, sans écriture."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REGISTRY=Path(__file__).resolve().parents[1]/'docs'/'data'/'platform-access-registry.v1.json'

def load_registry(path=REGISTRY):
    doc=json.loads(Path(path).read_text(encoding='utf-8'))
    if doc.get('schema')!='koa.daat.platform-access-registry.v1':
        raise ValueError('Unexpected platform access registry schema')
    return doc

def search(registry, *, query=None, family=None, only_checked=False):
    matches=[]
    for p in registry['platforms']:
        if query and query.casefold() not in (p['platform']+' '+p['id']).casefold():
            continue
        if family and family.zfill(2) not in p['family_ids']:
            continue
        if only_checked and p['platform_doc_status']!='official_docs_checked':
            continue
        matches.append(p)
    return matches

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',help='Recherche par nom de plateforme')
    p.add_argument('--family',help='ID 01..36 des familles de sources')
    p.add_argument('--only-checked',action='store_true',help='Documentation fournisseur consultée')
    p.add_argument('--json',action='store_true',help='Résultats JSON pour lecture machine')
    args=p.parse_args(argv)
    doc=load_registry()
    found=search(doc,query=args.query,family=args.family,only_checked=args.only_checked)
    if args.json:
        print(json.dumps(found,ensure_ascii=False,indent=2))
        return 0
    print(f"DaAT — {len(found)} profils, registre lecture seule (pas connecteurs actifs)\n")
    for r in found:
        print(f"{r['platform']}  [{','.join(r['family_ids'])}]  {r['platform_doc_status']}")
        print(f"  Voies: {', '.join(a['mode'] for a in r['access_paths'])}")
        print(f"  Priorité: {r['preferred_path']} | ChatGPT: {r['chatgpt_policy']}")
        print(f"  Limites: {r['blocking_limits']}")
        print()
    return 0

if __name__=='__main__':
    raise SystemExit(main())
