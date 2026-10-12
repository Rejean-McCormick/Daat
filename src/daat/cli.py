"""Offline-only CLI. No network listener and no implicit credentials."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .contracts import verify_baseline,validate_owner,verify_payload_profile
from .alignment import evaluate
from .mapping import load_profile,map_file
from .util import load_json,write_json
from .errors import DaatError

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(prog='daat',description='DaaT local integration-contract toolkit (no deployed service)')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('verify-contracts',help='Verify pinned owner contracts and v6 lock')
    vm=sub.add_parser('validate-mapping');vm.add_argument('profile',type=Path)
    mm=sub.add_parser('map');mm.add_argument('profile',type=Path);mm.add_argument('input',type=Path);mm.add_argument('--out',type=Path)
    am=sub.add_parser('alignment-report');am.add_argument('profile',type=Path);am.add_argument('--out',type=Path)
    vi=sub.add_parser('validate-ik');vi.add_argument('kind',choices=['envelope','receipt','artifact-ref','export-manifest','build','ready']);vi.add_argument('input',type=Path)
    vb=sub.add_parser('validate-build');vb.add_argument('input',type=Path)
    args=parser.parse_args(argv)
    try:
        result:dict|None=None
        if args.command=='verify-contracts': result=verify_baseline()
        elif args.command=='validate-mapping':
            p,_,_=load_profile(args.profile)
            result={'profile':p['id']+'/'+p['version'],'status':'valid','implementation_status':'local draft mapping format'}
        elif args.command=='map': result=map_file(args.profile,args.input)
        elif args.command=='alignment-report': result=evaluate(args.profile)
        elif args.command=='validate-ik':
            validate_owner(args.kind,load_json(args.input)); result={'valid':True,'owner_schema':args.kind}
        elif args.command=='validate-build':
            verify_payload_profile(load_json(args.input));result={'valid':True,'IK_profile':'kristal.build.request/2.0.0'}
        if getattr(args,'out',None): write_json(args.out,result)
        else: print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))
        return 0
    except (DaatError,ValueError,TypeError,KeyError) as e:
        print(json.dumps({'ok':False,'code':getattr(e,'code','INPUT_ERROR'),'error':str(e)},ensure_ascii=False),file=sys.stderr)
        return 2

if __name__=='__main__':
    sys.exit(main())
