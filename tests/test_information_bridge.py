"""Evidence-grade offline tests for the complete new information-bridge path."""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime, timezone, timedelta
from pathlib import Path
import csv
import io
import json
import os
import tempfile
import zipfile
import pytest

from daat.information_bridge import (SourceRegistry,AccessPlanner,LocalIngestor,ContextBuilder,
                                     Rights,SourceItem,BridgeError,Limits,verify_export)
from daat.information_bridge.registry import CapabilityGrant
from daat.information_bridge.model import sha_text
from daat.information_bridge.network import RemotePolicy,check_url,get_paginated_json
from daat.information_bridge.collection import collect_json,collect_feed
from daat.information_bridge.ai_review import validate_response,correction_prompt
from daat.information_bridge.cli import build_from_job,main
from daat.information_bridge.context import validate_bundle
from daat.information_bridge.sync import Checkpoints,identify_duplicates

ACTIONS = ('read','copy','retain','transform','ai_disclosure')

def rights(**overrides):
    obj={a:'allowed' for a in ACTIONS}
    obj.update(basis='synthetic authorization fixture',evidence_ref='test-rights-001',
               attestation='operator_asserted',classification='public')
    obj.update(overrides)
    return Rights(**obj)

def source(platform='medium',kind='excerpt',revision='r1',external='https://example.invalid/p1',**r):
    return SourceItem(platform,external,revision,kind,rights(**r))

def demo():
    x=LocalIngestor()
    s=source()
    x.add_text(source=s,text='A clearly marked synthetic reading says that interpretations can disagree.',locator='test:1')
    return x,ContextBuilder(x.corpus).build('What can be inferred?',generated_at='2026-11-14T10:00:00Z')

@pytest.mark.parametrize('platform_id', list(SourceRegistry().profiles))
def test_every_platform_has_safe_explicit_access_decision(platform_id):
    registry=SourceRegistry()
    p=registry.get(platform_id)
    assert all(x['mode'] in registry.data['method_legend'] for x in p['access_paths'])
    decision=AccessPlanner(registry).plan(platform_id)
    assert decision['result']=='blocked'
    assert decision['selected_method'] is None
    assert decision['canonical_authority'] is False

@pytest.mark.parametrize('right',ACTIONS)
def test_one_missing_right_excludes_text(right):
    x=LocalIngestor()
    r={right:'unknown'}
    if right in ('read','copy','transform'):
        with pytest.raises(BridgeError):x.add_text(source=source(**r),text='synthetic content')
    else:
        x.add_text(source=source(**r),text='synthetic content')
        with pytest.raises(BridgeError) as exc:ContextBuilder(x.corpus).build('question')
        assert exc.value.code=='CONTEXT_BLOCKED'

def test_expired_and_revoked_rights_are_blocked():
    yesterday=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat()
    assert rights(expires_at=yesterday).can_export_text() is False
    assert rights(revoked=True).can_export_text() is False
    assert rights(attestation='unverified').can_export_text() is False

def test_manual_assertion_cannot_unlock_approved_ai_host():
    assert rights().can_export_text('approved_ai_host') is False
    assert rights(attestation='host_verified').can_export_text('approved_ai_host') is True

def test_reference_only_does_not_hallucinate_full_text():
    x=LocalIngestor();x.add_reference(source(kind='reference_only'))
    b=ContextBuilder(x.corpus).build('Discuss this article')
    assert not b['fragments'] and 'référence seule' in ' '.join(b['uncertainties'])
    with pytest.raises(BridgeError):x.add_text(source=source(kind='reference_only',revision='r2'),text='unread article')

def test_bundle_roundtrip_and_tamper_refusal(tmp_path):
    x,b=demo();target=tmp_path/'export'
    ContextBuilder(x.corpus).export(b,target)
    assert verify_export(target)['valid']
    assert 'DONNÉES NON FIABLES' in (target/'prompt-chatgpt.md').read_text()
    with (target/'context-bundle.json').open('a') as out:out.write('changed')
    with pytest.raises(BridgeError): verify_export(target)
    with pytest.raises(BridgeError):ContextBuilder(x.corpus).export(b,target)

def test_content_tamper_while_recalculating_fragment_hash_still_needs_integrity(tmp_path):
    x,b=demo()
    b['fragments'][0]['text']+=' an invented claim'
    with pytest.raises(BridgeError):validate_bundle(b)

def test_secret_is_not_exported():
    x=LocalIngestor();x.add_text(source=source(),text='A key: ghp_abcdefghijklmnopqrstuvwxyz1234567890')
    b=ContextBuilder(x.corpus).build('question')
    assert not b['fragments']
    assert any('possible_secret' in z for z in b['disclosure']['excluded_reasons'])

def test_private_external_identity_is_redacted():
    x=LocalIngestor();s=source(classification='confidential')
    x.add_text(source=s,text='Confidential author-provided text authorized for manual use')
    b=ContextBuilder(x.corpus).build('question')
    assert b['sources'][0]['external_id']=='[redacted-internal-reference]'

def test_context_budget_is_deterministic():
    x=LocalIngestor(limits=Limits(max_fragment_chars=700))
    x.add_text(source=source(),text='a'*1400)
    b=ContextBuilder(x.corpus,limits=Limits(max_context_chars=2000)).build('question')
    assert len(b['fragments'])==1
    assert any('budget_exhausted' in s for s in b['disclosure']['excluded_reasons'])

@pytest.mark.parametrize('bad',[
    {'attestation':'bogus'}, {'classification':'secret'}, {'read':'yes'},
    {'basis':'', 'read':'allowed'}, {'evidence_ref':'token=abcde1234567890123'}
])
def test_invalid_rights_refused(bad):
    with pytest.raises(BridgeError):rights(**bad)

def test_synthetically_eligible_local_grant_not_secretly_owner_certified():
    reg=SourceRegistry()
    grant=CapabilityGrant('medium','manual_paste',rights(),implementation_tested=True)
    result=AccessPlanner(reg).plan('medium',[grant])
    assert result['result']=='eligible'
    assert result['selected_method']=='manual_paste'
    assert result['canonical_authority'] is False

def test_rss_metadata_only_and_remote_contract_enforcement():
    class Fake:
        def get(self,url,headers=None):
            return 200,{},b'<rss><channel><item><title>T</title><description>Short summary.</description><guid>A</guid></item></channel></rss>'
    grant=CapabilityGrant('medium','rss_atom',rights(attestation='host_verified'),True,True,'owner-test-contract')
    x=collect_feed('https://medium.com/feed/test','medium',grant,Fake())
    assert len(x.corpus.sources)==1
    assert x.corpus.sources[0].content_kind=='abstract'
    assert all('full_text' not in f.content_kind for f in x.corpus.fragments)
    with pytest.raises(BridgeError):collect_feed('https://medium.com/feed','medium',
        CapabilityGrant('medium','rss_atom',rights(),True,False),Fake())

def test_json_adapter_reports_metadata_not_article():
    class Fake:
        def get(self,url,headers=None):
            return 200,{'etag':'r1'},json.dumps({'results':[{'id':'doi:10/x','title':'hello'}]}).encode()
    grant=CapabilityGrant('philpapers','api_read',rights(attestation='host_verified'),True,True,'owner-test-contract')
    x=collect_json('https://philpapers.org/api','philpapers',grant,Fake())
    assert x.corpus.sources[0].content_kind=='structured_record'

@pytest.mark.parametrize('url',["http://medium.com/x","https://127.0.0.1/a",
    "https://user:pass@medium.com/x","https://other.invalid/x",
    "https://medium.com/x?token=abc", "https://medium.com/x#fragment"])
def test_remote_url_refusal(url):
    with pytest.raises(BridgeError):check_url(url,RemotePolicy(('medium.com',),True))

def test_network_disabled_by_default():
    with pytest.raises(BridgeError):check_url('https://medium.com/feed/x',RemotePolicy(('medium.com',)))

def test_bounded_pagination_and_host_guard():
    class Fake:
        def get(self,url,headers=None):
            if url.endswith('/1'):
                return 200,{},b'{"items":[{"id":"1"}],"next":"https://provider.test/2"}'
            return 200,{},b'{"items":[{"id":"2"}]}'
    items,history=get_paginated_json(Fake(),'https://provider.test/1')
    assert len(items)==2 and len(history)==2
    class HostEscape:
        def get(self,url,headers=None):
            return 200,{},b'{"items":[],"next":"https://evil.test/2"}'
    with pytest.raises(BridgeError):get_paginated_json(HostEscape(),'https://provider.test/1')

def test_text_and_xml_and_bibliography_paths(tmp_path):
    (tmp_path/'sample.html').write_text('<article><p>Hello <b>world</b></p><script>evil()</script></article>')
    (tmp_path/'sample.ris').write_text('TY  - JOUR\nTI  - A paper\nDO  - 10.1234/a\nER  - \n')
    (tmp_path/'sample.rss').write_text('<rss><channel><item><title>Notice</title><description>Summary</description></item></channel></rss>')
    x=LocalIngestor()
    x.add_file(root=tmp_path,relative_path='sample.html',source=source(kind='full_text_authorized',revision='h1'))
    x.add_file(root=tmp_path,relative_path='sample.ris',source=source(kind='structured_record',revision='r2'))
    x.add_file(root=tmp_path,relative_path='sample.rss',source=source(kind='abstract',revision='r3'))
    assert 'evil()' not in ''.join(f.text for f in x.corpus.fragments)
    assert len(x.corpus.sources)==3
    assert len(x.corpus.fragments)>=3

def test_xml_external_entity_refused(tmp_path):
    (tmp_path/'evil.xml').write_bytes(b'<!DOCTYPE foo [ <!ENTITY x SYSTEM "file:///etc/passwd">]><foo>&x;</foo>')
    with pytest.raises(BridgeError):LocalIngestor().add_file(root=tmp_path,relative_path='evil.xml',source=source(kind='structured_record'))

def test_csv_and_jsonl_are_records_without_fake_quote_verification(tmp_path):
    (tmp_path/'a.csv').write_text('a,b\n1,2\n')
    x=LocalIngestor();x.add_file(root=tmp_path,relative_path='a.csv',source=source(kind='structured_record'))
    assert x.corpus.records and all(not f.quote_verified for f in x.corpus.fragments)
    with pytest.raises(BridgeError):LocalIngestor().add_file(root=tmp_path,relative_path='a.csv',source=source(kind='full_text_authorized'))

def test_medium_zip_html_and_traversal_rejection(tmp_path):
    with zipfile.ZipFile(tmp_path/'my-posts.zip','w') as z:
        z.writestr('posts/one.html','<article><h1>Post A</h1><p>Owner post text.</p></article>')
        z.writestr('posts/two.html','<article><p>Another post.</p></article>')
    x=LocalIngestor();x.add_file(root=tmp_path,relative_path='my-posts.zip',source=source(kind='full_text_authorized'))
    assert len(x.corpus.fragments)==2
    assert 'posts/one.html' in x.corpus.fragments[0].locator
    with zipfile.ZipFile(tmp_path/'bad.zip','w') as z:z.writestr('../steal.txt','bad')
    with pytest.raises(BridgeError):LocalIngestor().add_file(root=tmp_path,relative_path='bad.zip',
                                             source=source(kind='full_text_authorized'))

def test_path_escape_and_symlink_rejected(tmp_path):
    (tmp_path/'safe.txt').write_text('safe')
    x=LocalIngestor()
    with pytest.raises(BridgeError):x.add_file(root=tmp_path,relative_path='../outside.txt',source=source())
    if hasattr(os,'symlink'):
        try:(tmp_path/'link.txt').symlink_to(tmp_path/'safe.txt')
        except OSError:pass
        else:
            with pytest.raises(BridgeError):x.add_file(root=tmp_path,relative_path='link.txt',source=source())

def test_ai_response_requires_exact_attributed_quote_and_review():
    _,b=demo(); frag=b['fragments'][0]
    r={'schema':'daat.ai-reading-response/1.0-local-proposed','bundle_id':b['manifest']['bundle_id'],
       'items':[{'id':'one','kind':'observation','statement':'Attributed summary',
       'citations':[{'fragment_id':frag['fragment_id'],'exact_quote':'interpretations can disagree'}],
       'uncertainties':[]}],'open_questions':[]}
    audit=validate_response(b,r)
    assert audit['accepted_as']=='untrusted_draft_for_human_review'
    r['items'][0]['citations'][0]['exact_quote']='invented fake'
    with pytest.raises(BridgeError):validate_response(b,r)
    r['items'][0]['citations'][0]['exact_quote']='interpretations can disagree'
    r['items'][0]['canonical']='yes'
    with pytest.raises(BridgeError):validate_response(b,r)

def test_checkpoint_tenant_isolation_idempotence_revocation(tmp_path):
    db=tmp_path/'state.sqlite'
    a=Checkpoints(db,'tenant-A');b=Checkpoints(db,'tenant-B')
    a.put('job','src-1','rev1','page:2',metadata={'secret':'not persisted'})
    assert b.get('job','src-1') is None
    assert a.get('job','src-1')['state']=='REFERENCED'
    assert a.observe('doc','rev1',{'data':'hi'})=='new'
    assert a.observe('doc','rev1',{'data':'hi'})=='duplicate'
    assert a.observe('doc','rev1',{'data':'different'})=='revision_conflict'
    a.put('job','src-1','rev1',None,state='REVOKED')
    with pytest.raises(BridgeError):a.put('job','src-1','rev1',None,state='NORMALIZED')
    assert b.observe('doc','rev1',{'data':'hi'})=='new'
    assert b'secret' not in db.read_bytes()

def test_candidate_duplicates_never_become_canonical():
    a=source('philpapers','abstract','v1','doi:10.1111/example')
    b=source('openalex','abstract','v1','https://doi.org/10.1111/example')
    d=identify_duplicates([a,b])
    assert d['review_candidates'] and not d['review_candidates'][0]['canonical_match']

def test_cli_end_to_end_offline(tmp_path,capsys):
    input_dir=tmp_path/'input';input_dir.mkdir()
    (input_dir/'article.md').write_text('A synthetic text supplied by a consenting author.',encoding='utf-8')
    manifest={'question':'Compare the available evidence','language':'fr',
      'sources':[{'platform_id':'medium','external_id':'export://author/article',
                  'revision':'post-1','content_kind':'full_text_authorized',
                  'rights':{a:'allowed' for a in ACTIONS} | {'basis':'synthetic_fixture','evidence_ref':'synthetic-right-01',
                  'attestation':'operator_asserted','classification':'public'},
                  'path':'article.md','acquired_via':'user_export'},
                  {'platform_id':'philpapers','external_id':'doi:10.123/summary','revision':'r1',
                   'content_kind':'reference_only',
                   'rights':{a:'unknown' for a in ACTIONS},
                   }]}
    (input_dir/'job.json').write_text(json.dumps(manifest))
    out=tmp_path/'output'
    result=build_from_job(input_dir/'job.json',input_dir,out)
    assert result['sources']==2 and result['fragments']==1
    assert result['excluded']==1 and verify_export(out)['valid']
    assert main(['verify','--dir',str(out)])==0
    assert 'true' in capsys.readouterr().out.lower()


def test_office_docx_xlsx_pptx_and_formula_never_executed(tmp_path):
    def zipped(path,data):
        with zipfile.ZipFile(path,'w') as z:
            for k,v in data.items(): z.writestr(k,v)
    zipped(tmp_path/'a.docx',{'word/document.xml':
        '<w:document xmlns:w="urn:w"><w:body><w:p><w:r><w:t>Owner report</w:t></w:r></w:p></w:body></w:document>'})
    zipped(tmp_path/'a.xlsx',{'xl/sharedStrings.xml':
        '<sst><si><t>Balance</t></si></sst>',
        'xl/worksheets/sheet1.xml':
        '<worksheet><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><f>2+2</f><v>4</v></c></row></sheetData></worksheet>'})
    zipped(tmp_path/'a.pptx',{'ppt/slides/slide1.xml':
        '<a:spTree xmlns:a="urn:a"><a:p><a:r><a:t>Presentation slide</a:t></a:r></a:p></a:spTree>'})
    ing=LocalIngestor()
    ing.add_file(root=tmp_path,relative_path='a.docx',source=source(kind='full_text_authorized',revision='doc'))
    ing.add_file(root=tmp_path,relative_path='a.xlsx',source=source(kind='structured_record',revision='xlsx'))
    ing.add_file(root=tmp_path,relative_path='a.pptx',source=source(kind='excerpt',revision='pptx'))
    texts=' '.join(f.text for f in ing.corpus.fragments)
    assert 'Owner report' in texts and 'Balance' in texts and 'Presentation slide' in texts
    assert '[formula-not-executed]' in texts
    assert all(not f.quote_verified for f in ing.corpus.fragments)

def test_eml_text_only_no_attachments(tmp_path):
    from email.message import EmailMessage
    msg=EmailMessage(); msg['Subject']='Private example'
    msg.set_content('Hello, authorized mail body.')
    msg.add_attachment(b'CONFIDENTIAL BINARY',maintype='application',subtype='octet-stream',filename='payload.bin')
    (tmp_path/'note.eml').write_bytes(msg.as_bytes())
    ing=LocalIngestor();ing.add_file(root=tmp_path,relative_path='note.eml',source=source(kind='excerpt'))
    text=''.join(f.text for f in ing.corpus.fragments)
    assert 'authorized mail body' in text and 'CONFIDENTIAL BINARY' not in text

def test_oai_resumption_and_deleted_metadata_only():
    from daat.information_bridge.collection import collect_oai_pages
    body1=b'<OAI-PMH><ListRecords><record><header><identifier>oai:one</identifier></header><metadata><title>First</title></metadata></record><resumptionToken>next01</resumptionToken></ListRecords></OAI-PMH>'
    body2=b'<OAI-PMH><ListRecords><record><header status="deleted"><identifier>oai:two</identifier></header></record></ListRecords></OAI-PMH>'
    class Fake:
        def get(self,url,headers=None):return 200,{},body2 if 'resumptionToken' in url else body1
    grant=CapabilityGrant('philpapers','harvest_oai_pmh',rights(attestation='host_verified'),True,True,'synthetic-owner')
    x=collect_oai_pages('https://philpapers.org/oai?verb=ListRecords&metadataPrefix=oai_dc',
                        'philpapers',grant,Fake())
    assert len(x.corpus.sources)==2
    assert x.corpus.sources[1].content_kind=='reference_only'
    assert all(f.content_kind!='full_text_authorized' for f in x.corpus.fragments)

def test_diagnostic_is_honest_and_covers_full_registry():
    from daat.information_bridge.diagnostic import readiness
    d=readiness()
    assert d['registry']['profiles']==89
    assert d['registry']['families']==36
    assert d['result']=='NOT_PRODUCTION_QUALIFIED'
    assert all(not p['owner_connector_certified'] for p in d['platforms'])

def test_unsafe_office_zip_denied(tmp_path):
    with zipfile.ZipFile(tmp_path/'bad.docx','w') as z:z.writestr('../unsafe.xml','<doc/>')
    with pytest.raises(BridgeError):LocalIngestor().add_file(root=tmp_path,relative_path='bad.docx',source=source())

def test_philpapers_and_medium_multisource_abstract_vs_author_export(tmp_path):
    (tmp_path/'philpapers.ris').write_text('TY  - JOUR\nTI  - Synthetic scholarly article\nDO  - 10.5555/example\nER  - \n')
    with zipfile.ZipFile(tmp_path/'medium-export.zip','w') as z:
        z.writestr('posts/a.html','<article><p>My complete article, explicitly supplied.</p></article>')
    ing=LocalIngestor()
    ing.add_file(root=tmp_path,relative_path='philpapers.ris',source=source('philpapers','structured_record','bibv1','doi:10.5555/example'))
    ing.add_file(root=tmp_path,relative_path='medium-export.zip',source=source('medium','full_text_authorized','mv1','account-export:me'))
    out=tmp_path/'output'
    b=ContextBuilder(ing.corpus).build('What do these actual representations establish?')
    ContextBuilder(ing.corpus).export(b,out)
    assert verify_export(out)['valid']
    assert len(b['sources'])==2
    assert not any(f['content_kind']=='full_text_authorized' and f['source_ref']==ing.corpus.sources[0].ref()
                   for f in b['fragments'])
    assert 'medium-export.zip#posts/a.html' in b['fragments'][-1]['locator']

def test_context_batch_never_drops_eligible_fragments(tmp_path):
    from daat.information_bridge.batching import ContextBatcher
    limits=Limits(max_fragment_chars=350,max_total_chars=30000,max_context_chars=3700)
    ing=LocalIngestor(limits=limits)
    ing.add_text(source=source(),text='reliable synthetic text. '*400)
    expected=len(ing.corpus.fragments)
    parts=ContextBatcher(ing.corpus,limits).build_many('What does the source actually say?')
    all_ids=[f['fragment_id'] for p in parts for f in p['fragments']]
    assert len(parts)>1
    assert len(all_ids)==expected and len(all_ids)==len(set(all_ids))
    out=tmp_path/'batch'
    index=ContextBatcher(ing.corpus,limits).export_many('What does the source actually say?',out)
    assert len(index['parts'])==len(parts)
    for part in index['parts']:
        assert verify_export(out/part['relative_directory'])['valid']

def test_prompt_response_bundle_id_matches_after_context_budget_trim():
    x=LocalIngestor(limits=Limits(max_fragment_chars=700))
    x.add_text(source=source(),text='a'*1400)
    b=ContextBuilder(x.corpus,limits=Limits(max_context_chars=2000)).build('question')
    assert len(b['fragments'])==1
    assert b['manifest']['bundle_id'] in b['prompts'][0]['text']
    assert b['manifest']['bundle_id'] in __import__('daat.information_bridge.context',fromlist=['prompt_for']).prompt_for(b)


def test_private_evidence_identifier_is_not_disclosed():
    x=LocalIngestor()
    s=source(classification='internal',evidence_ref='internal-file:///private/evidence-123')
    x.add_text(source=s,text='Private reference can still be quoted by authorized operator')
    b=ContextBuilder(x.corpus).build('question')
    assert b['sources'][0]['rights_evidence_ref'].startswith('sha256:')
    assert 'private/evidence-123' not in json.dumps(b)


def test_manual_ai_review_export_is_draft_and_immutable(tmp_path):
    from daat.information_bridge.ai_review import save_review
    _,b=demo()
    fragment=b['fragments'][0]
    quoted=fragment['text'][0:12]
    response={'schema':'daat.ai-reading-response/1.0-local-proposed','bundle_id':b['manifest']['bundle_id'],
       'items':[{'id':'r1','kind':'observation','statement':'Attribution bornée',
                 'citations':[{'fragment_id':fragment['fragment_id'],'exact_quote':quoted}],
                 'uncertainties':['Non vérifié au-delà du fragment']}],'open_questions':[]}
    dest=tmp_path/'review'
    result=save_review(b,response,dest)
    assert result['authority']=='none'
    assert (dest/'audit.json').is_file() and (dest/'integrity.json').is_file()
    with pytest.raises(BridgeError):save_review(b,response,dest)


def test_original_example_job_runs_as_a_local_multisource_demo(tmp_path):
    root=Path(__file__).resolve().parents[1] / 'examples' / 'information-bridge'
    result=build_from_job(root/'example-job.json',root,tmp_path/'demo')
    assert result['included_sources']==2 and result['excluded']>=1
    assert result['disclosed'] is False
    assert verify_export(tmp_path/'demo')['valid'] is True
