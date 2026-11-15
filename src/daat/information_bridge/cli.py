"""DaaT information bridge CLI. Offline, noncanonical, no implicit network access."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from importlib.resources import files
from jsonschema import Draft202012Validator,FormatChecker
from typing import Any, Callable

from .model import BridgeError, Rights, SourceItem, Limits
from .registry import SourceRegistry, AccessPlanner, CapabilityGrant
from .ingest import LocalIngestor
from .context import ContextBuilder, verify_export
from .ai_review import validate_response, correction_prompt, response_template, save_review
from .sync import identify_duplicates
from .diagnostic import readiness
from .batching import ContextBatcher


def _read_json(path:Path)->Any:
    if path.stat().st_size>6_000_000:
        raise BridgeError('MANIFEST_LIMIT','JSON input file exceeds 6 MB')
    return json.loads(path.read_text(encoding='utf-8'))


def load_job_data(job:dict[str,Any], root:Path, *, progress:Callable[[int,int,str],None]|None=None,
             limits:Limits|None=None):
    schema=json.loads(files('daat').joinpath('resources','contracts','daat','source-job.schema.json').read_text(encoding='utf-8'))
    errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(job))
    if errors:
        raise BridgeError('JOB_SCHEMA',errors[0].message)
    if not isinstance(job,dict) or set(job)-{'question','language','sources','max_context_chars'} or not isinstance(job.get('sources'),list):
        raise BridgeError('JOB_INVALID','Expected question, language and bounded sources')
    if not 1<=len(job['sources'])<=500:
        raise BridgeError('JOB_INVALID','Expected 1..500 sources')
    registry=SourceRegistry()
    cap=limits or Limits()
    ing=LocalIngestor(limits=cap)
    total=len(job['sources'])
    for index,s in enumerate(job['sources'],1):
        if not isinstance(s,dict) or not isinstance(s.get('rights'),dict):
            raise BridgeError('JOB_INVALID','Source rights are mandatory')
        platform=s.get('platform_id')
        registry.get(platform)
        rights=Rights(**s['rights'])
        src=SourceItem(platform_id=platform,external_id=s['external_id'],revision=s['revision'],
             content_kind=s['content_kind'],rights=rights,
             title=s.get('title',''),author=s.get('author',''),
             acquired_via=s.get('acquired_via','user_paste'))
        if src.content_kind=='reference_only':
            if 'text' in s or 'path' in s:
                raise BridgeError('JOB_INVALID','Reference-only items cannot declare content')
            ing.add_reference(src)
        elif 'text' in s and 'path' not in s:
            if not isinstance(s['text'],str):raise BridgeError('JOB_INVALID','Source text must be string')
            ing.add_text(source=src,text=s['text'],locator='user-supplied',quote_verified=True)
        elif 'path' in s and 'text' not in s:
            ing.add_file(root=root,relative_path=s['path'],source=src,
                         git_commit=s.get('git_commit'))
        else:
            raise BridgeError('JOB_INVALID','Exactly one source content path or text required')
        if progress:progress(index,total,src.ref())
    return ing.corpus,job



def load_job(path:Path, root:Path, *, progress:Callable[[int,int,str],None]|None=None,
             limits:Limits|None=None):
    return load_job_data(_read_json(path),root,progress=progress,limits=limits)

def build_from_job(job_path:Path,root:Path,out:Path,*,progress=None)->dict:
    corpus,job=load_job(job_path,root,progress=progress)
    limits=Limits(max_context_chars=int(job.get('max_context_chars',70000)))
    ctx=ContextBuilder(corpus,limits=limits).build(job['question'],language=job.get('language','fr'))
    ContextBuilder(corpus,limits=limits).export(ctx,out)
    return {'bundle_id':ctx['manifest']['bundle_id'], 'sources':len(corpus.sources),
            'included_sources':len(ctx['sources']),'fragments':len(ctx['fragments']),
            'excluded':len(ctx['disclosure']['excluded_reasons']),
            'export':str(out), 'authority':'none', 'disclosed':False,
            'review':'required', 'duplicate_candidates':len(identify_duplicates(corpus.sources)['review_candidates'])}



def build_from_data(job:dict[str,Any],root:Path,out:Path,*,progress=None)->dict:
    """Build directly in memory (GUI avoids writing plaintext pasted content to disk)."""
    corpus,parsed=load_job_data(job,root,progress=progress)
    limits=Limits(max_context_chars=int(parsed.get('max_context_chars',70000)))
    builder=ContextBuilder(corpus,limits=limits)
    bundle=builder.build(parsed['question'],language=parsed.get('language','fr'))
    builder.export(bundle,out)
    return {'bundle_id':bundle['manifest']['bundle_id'],'sources':len(corpus.sources),
            'fragments':len(bundle['fragments']), 'excluded':len(bundle['disclosure']['excluded_reasons']),
            'export':str(out), 'disclosed':False,'human_review':'required'}

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(prog='daat-bridge',description='DaaT information to ChatGPT context; no Kristal creation')
    sub=parser.add_subparsers(dest='action',required=True)
    catalog=sub.add_parser('catalog',help='Search the 89-platform offline catalogue')
    catalog.add_argument('--query',default='')
    plan=sub.add_parser('plan',help='Explain candidate routes; never grants rights')
    plan.add_argument('--platform',required=True); plan.add_argument('--desired',default='reference_only')
    build=sub.add_parser('build',help='Process explicitly authorized local job manifest')
    build.add_argument('--job',type=Path,required=True);build.add_argument('--root',type=Path,required=True)
    build.add_argument('--out',type=Path,required=True)
    batch=sub.add_parser('build-batch',help='Split large authorized corpora into complete stable prompt parts')
    batch.add_argument('--job',type=Path,required=True);batch.add_argument('--root',type=Path,required=True)
    batch.add_argument('--out',type=Path,required=True)
    verify=sub.add_parser('verify',help='Recompute file and bundle integrity')
    verify.add_argument('--dir',type=Path,required=True)
    review=sub.add_parser('review-response',help='Validate manual ChatGPT JSON candidate response')
    review.add_argument('--dir',type=Path,required=True);review.add_argument('--response',type=Path,required=True)
    review.add_argument('--save-to',type=Path,help='Optional new directory for unsigned AI review feedback')
    template=sub.add_parser('response-template',help='Print response prompt for ChatGPT')
    template.add_argument('--dir',type=Path,required=True)
    diag=sub.add_parser('diagnose',help='Readiness report for 89 profiles and the optional export')
    diag.add_argument('--dir',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.action=='catalog':
            registry=SourceRegistry()
            result=[{'id':p['id'],'name':p['platform'],'methods':[x['mode'] for x in p['access_paths']],
                     'connector_status':p['daat_connector_status']} for p in registry.search(args.query)]
            print(json.dumps({'count':len(result),'platforms':result},ensure_ascii=False,indent=2))
        elif args.action=='plan':
            print(json.dumps(AccessPlanner(SourceRegistry()).plan(args.platform,desired_kind=args.desired),
                             ensure_ascii=False,indent=2))
        elif args.action=='build':
            print(json.dumps(build_from_job(args.job,args.root,args.out),ensure_ascii=False,indent=2))
        elif args.action=='diagnose':
            print(json.dumps(readiness(args.dir),ensure_ascii=False,indent=2))
        elif args.action=='build-batch':
            corpus,job=load_job(args.job,args.root)
            cap=Limits(max_context_chars=int(job.get('max_context_chars',70000)))
            print(json.dumps(ContextBatcher(corpus,cap).export_many(job['question'],args.out,
                             language=job.get('language','fr')),ensure_ascii=False,indent=2))
        elif args.action=='verify':
            print(json.dumps(verify_export(args.dir),ensure_ascii=False,indent=2))
        elif args.action in ('review-response','response-template'):
            verify_export(args.dir)
            bundle=_read_json(args.dir/'context-bundle.json')
            if args.action=='review-response':
                response=_read_json(args.response)
                result=save_review(bundle,response,args.save_to) if args.save_to else validate_response(bundle,response)
                print(json.dumps(result,ensure_ascii=False,indent=2))
            else:
                print(response_template(bundle))
        return 0
    except (BridgeError,OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'ERROR','code':getattr(exc,'code','INPUT_ERROR'),
                 'message':str(exc)[:500],'no_remote_write':True},ensure_ascii=False),file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
