"""Transparent per-capability adaptation measures; not a quality rating."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .mapping import load_profile,apply,WEIGHTS
from .util import load_json,json_digest
from .errors import MappingError

def evaluate(profile_path:Path,*,golden:bool=True)->dict:
    profile,src,dst=load_profile(profile_path)
    fp=profile['field_policy']; rules=profile['rules']
    obligations=set(fp['required_target_obligations'])
    verified=False
    if golden and 'golden_input' in profile and 'golden_expected' in profile:
        base=Path(profile_path).resolve().parent
        for k in ('golden_input','golden_expected'):
            candidate=(base/profile[k]).resolve()
            if not candidate.is_relative_to(base) or not candidate.is_file():
                raise MappingError('MAPPING_PATH_INVALID','Golden fixture not found under mapping folder')
        observed=apply(profile,src,dst,load_json(base/profile['golden_input']))
        expected=load_json(base/profile['golden_expected'])
        if observed!=expected: raise MappingError('GOLDEN_MISMATCH','Output does not match golden fixture')
        verified=True
    covered=set(r['obligation'] for r in rules)&obligations
    burden=sum(WEIGHTS[r['class']] for r in rules)
    losses=len(fp['exclusions'])
    unsupported=sorted(obligations-covered)
    n=len(obligations)
    report={
      'format':'daat.alignment-report/0.2.0-draft',
      'profile':profile['id']+'/'+profile['version'],
      'capability_scope':profile['capabilities'],
      'method':'weighted-rule-inventory/0.2.0-draft',
      'pins':{'source':profile['source_contract']['ref'],'target':profile['target_contract']['ref'],
              'source_sha256':profile['source_contract']['sha256'],'target_sha256':profile['target_contract']['sha256']},
      'obligations':{'total':n,'supported':len(covered) if verified else 0,'unsupported_mandatory':unsupported},
      'coverage':(len(covered)/n if verified and n else 0),
      'burden_points':burden,'burden_per_obligation':burden/n if n else None,
      'loss_count':losses,'ambiguous_count':0,
      'zero_semantic_transform':burden==0 and losses==0 and not unsupported,
      'golden_verified':verified,
      'conformant_for_scope':False,
      'conformance_note':'Full IK/security/owner TCK not executed; no product quality score.',
      'transforms':[{'op':r['op'],'class':r['class'],'from':r['from'],'to':r['to'],
                     'obligation':r['obligation'],'burden':WEIGHTS[r['class']]} for r in rules],
      'exclusions':fp['exclusions'],
      'assessment_scope':'declared capability and golden fixture only; upstream preprocessing not independently audited'
    }
    report['report_digest_sha256']=json_digest(report)
    return report
