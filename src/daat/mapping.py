"""Strict declarative mapping. Never reads URLs or executes user-supplied code."""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal,InvalidOperation
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator,FormatChecker
from .util import load_json,file_digest
from .errors import MappingError

ROOT=Path(__file__).resolve().parents[2]
_BUNDLED_SCHEMA=Path(__file__).resolve().parent/'resources'/'contracts'/'daat'/'mapping-profile.schema.json'
_REPO_SCHEMA=ROOT/'contracts'/'daat'/'mapping-profile.schema.json'
WEIGHTS={'identity':0,'alias':1,'structural':2,'value':2,'contextual':4}
MISSING=object()

def parts(name: str) -> list[str]:
    if not isinstance(name,str) or not name or any(not x.isidentifier() or x.startswith('_') for x in name.split('.')):
        raise MappingError('MAPPING_PATH_INVALID','Path must be dotted public identifiers')
    return name.split('.')

def get_path(obj:dict,name:str) -> Any:
    current:Any=obj
    for part in parts(name):
        if not isinstance(current,dict) or part not in current: return MISSING
        current=current[part]
    return current

def put_path(result:dict,name:str,value:Any) -> None:
    chain=parts(name)
    current=result
    for token in chain[:-1]:
        if token not in current: current[token]={}
        if not isinstance(current[token],dict): raise MappingError('MAPPING_COLLISION','Conflicting structural output')
        current=current[token]
    if chain[-1] in current: raise MappingError('MAPPING_COLLISION','Duplicate destination path')
    current[chain[-1]]=deepcopy(value)

def _schema_validate(schema:dict,obj:Any) -> None:
    # Mapping-pack schemas are offline fixtures; never resolve remote or file references.
    def inspect(node:Any)->None:
        if isinstance(node,dict):
            for k,v in node.items():
                if k in ('$dynamicRef','$recursiveRef') or (k=='$ref' and (not isinstance(v,str) or not v.startswith('#/'))):
                    raise MappingError('UNSAFE_SCHEMA_REF','External/dynamic schema resolution is forbidden')
                inspect(v)
        elif isinstance(node,list):
            for v in node:inspect(v)
    inspect(schema)
    errs=list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(obj))
    if errs:
        err=sorted(errs,key=lambda e:(list(map(str,e.absolute_path)),e.message))[0]
        raise MappingError('CONTRACT_DATA_INVALID','Document does not satisfy pinned schema: '+err.message)

def _file_within(base:Path,relative:str)->Path:
    path=(base/relative).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file() or path.is_symlink():
        raise MappingError('MAPPING_PATH_INVALID','Mapping file outside local profile folder or missing')
    return path

def load_profile(path:Path) -> tuple[dict,dict,dict]:
    path=Path(path).resolve()
    profile=load_json(path)
    spec=load_json(_REPO_SCHEMA if _REPO_SCHEMA.is_file() else _BUNDLED_SCHEMA)
    _schema_validate(spec,profile)
    source_schemas=[]
    for side in ('source_contract','target_contract'):
        ref=profile[side]
        sfile=_file_within(path.parent,ref['path'])
        if file_digest(sfile)!=ref['sha256']:
            raise MappingError('CONTRACT_PIN_MISMATCH','Schema pin mismatch: '+side)
        source_schemas.append(load_json(sfile))
    check_profile(profile)
    return profile,*source_schemas

def check_profile(p:dict)->None:
    rules=p['rules']
    destinations=set(); obligations=set()
    for r in rules:
        parts(r['from']); parts(r['to'])
        if r['to'] in destinations: raise MappingError('MAPPING_COLLISION','Repeated destination')
        destinations.add(r['to']); obligations.add(r['obligation'])
        op=r['op']; kind=r['class']
        permitted={'copy':{'identity'},'rename':{'alias','structural'},'map_enum':{'value'},'convert_unit':{'value'},'assert_equal':{'identity'}}
        if op not in permitted: raise MappingError('MAPPING_INVALID','Unapproved operator')
        if kind not in permitted[op]: raise MappingError('BURDEN_MISDECLARED','Rule class inconsistent with operation')
        if op=='copy' and r['from']!=r['to']: raise MappingError('BURDEN_MISDECLARED','Renaming is not identity')
        if op=='rename' and r['from']==r['to']: raise MappingError('BURDEN_MISDECLARED','Not a rename')
        if op=='map_enum' and (not isinstance(r.get('map'),dict) or not r['map']):
            raise MappingError('MAPPING_INVALID','Enum mapping table required')
        if op=='convert_unit' and ('factor' not in r or Decimal(r['factor'])<=0):
            raise MappingError('MAPPING_INVALID','Positive factor required')
        if op=='assert_equal' and 'equals' not in r: raise MappingError('MAPPING_INVALID','Explicit assertion value required')
    if not set(p['field_policy']['required_target_obligations']).issubset(obligations):
        raise MappingError('MAPPING_UNSUPPORTED','Required target obligation not mapped')
    excluded=[e['path'] for e in p['field_policy']['exclusions']]
    if len(set(excluded))!=len(excluded): raise MappingError('MAPPING_INVALID','Repeated exclusion')
    mapped=[r['from'] for r in rules]
    for name in p['field_policy']['must_preserve']:
        if name not in mapped or name not in destinations:
            raise MappingError('MAPPING_LOSS_FORBIDDEN','Mandatory preservation must map to itself')
        if not any(r['op']=='copy' and r['from']==name for r in rules):
            raise MappingError('MAPPING_LOSS_FORBIDDEN','Preserved data may not be modified')

def _all_leaf_paths(v:Any,prefix:str='') -> set[str]:
    if isinstance(v,dict):
        result=set()
        if not v: return {prefix} if prefix else set()
        for key,value in v.items(): result.update(_all_leaf_paths(value, f'{prefix}.{key}' if prefix else key))
        return result
    return {prefix}

def apply(profile:dict,source_schema:dict,target_schema:dict,data:dict)->dict:
    _schema_validate(source_schema,data)
    check_profile(profile)
    fp=profile['field_policy']; rules=profile['rules']; result={}
    included=set()
    for r in rules:
        v=get_path(data,r['from'])
        if v is MISSING: raise MappingError('MAPPING_MISSING','Declared source field missing: '+r['from'])
        included.add(r['from'])
        op=r['op']
        if op=='map_enum':
            if not isinstance(v,str) or v not in r['map']:
                raise MappingError('MAPPING_AMBIGUOUS','Unknown enum member')
            v=r['map'][v]
        elif op=='convert_unit':
            if isinstance(v,bool) or not isinstance(v,(int,float)):
                raise MappingError('MAPPING_INVALID','Conversion requires numeric value')
            try:
                new=Decimal(str(v))*Decimal(r['factor'])
                if not new.is_finite(): raise MappingError('MAPPING_INVALID','Nonfinite conversion result')
                v=int(new) if new==new.to_integral_value() else float(new)
            except (InvalidOperation,OverflowError) as e:
                raise MappingError('MAPPING_INVALID','Numeric conversion failed') from e
        elif op=='assert_equal':
            if v!=r['equals']: raise MappingError('MAPPING_ASSERTION_FAILED','Assertion failed')
        put_path(result,r['to'],v)
    leaves=_all_leaf_paths(data)
    def covered(path:str,declared:str)->bool:
        return path==declared or path.startswith(declared+'.')
    unmapped=[p for p in leaves if not any(covered(p,used) for used in included)]
    for name in unmapped:
        if not any(covered(name,x['path']) for x in fp['exclusions']):
            raise MappingError('MAPPING_LOSS_FORBIDDEN','Undeclared source field omission: '+name)
    for name in fp['must_preserve']:
        if get_path(data,name)!=get_path(result,name):
            raise MappingError('MAPPING_LOSS_FORBIDDEN','Required field not preserved')
    _schema_validate(target_schema,result)
    return result

def map_file(profile_path:Path,input_path:Path)->dict:
    p,source,target=load_profile(profile_path)
    data=load_json(input_path)
    return apply(p,source,target,data)
