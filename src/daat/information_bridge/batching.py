"""Context-window sharding without dropping eligible source fragments.

This produces multiple immutable local context bundles. It does not send any
request to ChatGPT and cannot schedule upstream collection.
"""
from __future__ import annotations
from dataclasses import replace
from pathlib import Path
import json
from typing import Any

from .model import BridgeError,Limits,digest,utcnow
from .ingest import PreparedCorpus
from .context import ContextBuilder,verify_export

class ContextBatcher:
    def __init__(self,corpus:PreparedCorpus,limits:Limits|None=None):
        self.corpus=corpus;self.limits=limits or Limits()

    def _subcorpus(self,fragments,first:bool):
        used={f.source_ref for f in fragments}
        sources=[s for s in self.corpus.sources if s.ref() in used or (first and
                  (s.content_kind=='reference_only' or not s.rights.can_export_text()))]
        return PreparedCorpus(sources=list(sources),fragments=list(fragments),
           records=[r for r in self.corpus.records if r.get('source_ref') in used],
           warnings=list(self.corpus.warnings) if first else [])

    def build_many(self,question:str,*,language:str='fr')->list[dict[str,Any]]:
        eligible={s.ref() for s in self.corpus.sources if s.rights.can_export_text()}
        fragments=[f for f in self.corpus.fragments if f.source_ref in eligible]
        if not eligible:
            raise BridgeError('CONTEXT_BLOCKED','No eligible source for disclosure')
        # Conservative room for headers. Actual full-prompt length is verified.
        budget=max(1,self.limits.max_context_chars-2500)
        groups=[];group=[];used=0
        for f in fragments:
            weight=len(f.text)+220
            if weight>budget:
                raise BridgeError('CONTEXT_FRAGMENT_TOO_LONG','Use smaller ingestion segments for this context limit')
            if group and used+weight>budget:
                groups.append(group);group=[];used=0
            group.append(f);used+=weight
        groups.append(group)
        outputs=[]
        i=0
        for group in groups:
            i+=1
            # Shrink the group if the complete prompt header exceeds estimate.
            while True:
                part=self._subcorpus(group,first=(i==1))
                data=ContextBuilder(part,limits=self.limits).build(question,language=language,version=i)
                if len(data['fragments'])==len(group):
                    outputs.append(data)
                    break
                if len(group)==1:
                    raise BridgeError('CONTEXT_FRAGMENT_TOO_LONG','One fragment cannot fit complete prompt')
                cut=max(1,len(group)//2)
                tail=group[cut:]
                group=group[:cut]
                groups.insert(i,tail)
                # ContextBuilder could have included fragments non-prefix? only suffix dropped.
        count=sum(len(part['fragments']) for part in outputs)
        if count!=len(fragments) or len({f['fragment_id'] for part in outputs for f in part['fragments']})!=count:
            raise BridgeError('BATCH_INTEGRITY','Fragment lost or repeated across shards')
        return outputs

    def export_many(self,question:str,out:Path,*,language:str='fr')->dict[str,Any]:
        if out.exists():raise BridgeError('OUTPUT_EXISTS','Batch directory must not exist')
        out.mkdir(parents=True)
        bundles=self.build_many(question,language=language)
        exports=[]
        for ix,b in enumerate(bundles,1):
            folder=out/f'part-{ix:03}'
            ContextBuilder(self.corpus,limits=self.limits).export(b,folder)
            verified=verify_export(folder)
            exports.append({'part':ix,'relative_directory':folder.name,
                  'bundle_id':verified['bundle_id'],'fragments':len(b['fragments'])})
        index={'schema':'daat.context-batch-index/1.0-local','created_at':utcnow(),
                'parts':exports,'authority':'noncanonical_unsigned','disclosed':False}
        (out/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
        return index
