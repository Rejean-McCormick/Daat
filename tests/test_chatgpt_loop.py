"""User-operated assistant loop: no source fetching, no owner authority."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from daat.chatgpt_loop import (
    make_bundle, validate_chatgpt_response, verify_bundle, make_repair_prompt,
    BUNDLE_FORMAT, DRAFT_FORMAT, RESPONSE_FORMAT,
)
from daat.errors import AdmissionError


def source(scope='summary', **changes):
    item = dict(provider='Medium', title='An example article',
                locator='https://medium.com/example/article', scope=scope,
                access_method='user_paste', rights_basis='Operator is permitted to share this example',
                text='The author argues that communication supports collaborative decision making.')
    item.update(changes)
    return item


def bundle(sources=None):
    return make_bundle(sources or [source()], purpose='Build reviewable noncanonical candidates',
                       user_rights_confirmed=True, chatgpt_disclosure_confirmed=True)


def response(b, quote='communication supports collaborative decision making'):
    return dict(format=RESPONSE_FORMAT, request_sha256=b['request_sha256'],
                candidate_parts=[dict(kind='claim', text='Selon cet auteur, la communication soutient les décisions collectives.',
                                      evidence=[dict(source_id=b['request']['sources'][0]['source_id'], quote=quote)],
                                      confidence=0.8, uncertainty='Affirmation attribuée; non vérifiée indépendamment.')],
                unknowns=['Le contenu intégral de l’article n’a pas été fourni.'])


def fail(code, fn, *a, **kw):
    with pytest.raises(AdmissionError) as err:
        fn(*a, **kw)
    assert err.value.code == code


def test_prompt_and_draft():
    b = bundle()
    assert b['format'] == BUNDLE_FORMAT
    assert 'scope vaut summary' in b['prompt']
    assert 'medium.com/example/article' in b['prompt']
    assert verify_bundle(b)['valid']
    draft = validate_chatgpt_response(b, response(b))
    assert draft['format'] == DRAFT_FORMAT
    assert draft['candidate_parts'][0]['review_state'] == 'pending_human_review'
    assert draft['candidate_parts'][0]['semantic_identity'] is None
    assert draft['candidate_parts'][0]['evidence'][0]['limited_to_supplied_material'] is True
    assert draft['owner_approval'] is None and draft['publication_authorized'] is False


def test_full_text_scope_is_only_a_user_declaration():
    b = bundle([source(scope='full_text')])
    draft = validate_chatgpt_response(b, response(b))
    assert draft['candidate_parts'][0]['evidence'][0]['source_scope'] == 'full_text'
    assert draft['candidate_parts'][0]['evidence'][0]['limited_to_supplied_material'] is False


def test_no_permission_to_use():
    fail('CHATGPT_RIGHTS_REQUIRED', make_bundle, [source()], purpose='X',
         user_rights_confirmed=False, chatgpt_disclosure_confirmed=True)


def test_no_permission_to_disclose_to_chatgpt():
    fail('CHATGPT_RIGHTS_REQUIRED', make_bundle, [source()], purpose='X',
         user_rights_confirmed=True, chatgpt_disclosure_confirmed=False)

@pytest.mark.parametrize('kwargs', [
    {'locator':'file:///etc/passwd'}, {'locator':'https://user:pass@example.com/path'},
    {'scope':'unknown'}, {'access_method':'scrape'}, {'text':'x'}, {'title':''},
    {'text':'x'*40001}, {'provider':''}])
def test_bad_source(kwargs):
    fail('CHATGPT_INPUT_INVALID', bundle, [source(**kwargs)])


def test_source_count_and_total_limit():
    fail('CHATGPT_INPUT_INVALID', bundle, [source()]*7)
    s1=source(text='x'*35000)
    s2=source(title='Second', text='y'*35000)
    s3=source(title='Third', text='z'*35000)
    fail('CHATGPT_BUNDLE_INVALID', bundle, [s1, s2, s3])


def test_multi_source_success():
    b = bundle([source(),source(provider='PhilPapers', title='A bibliographic abstract',
                                 text='The paper provides a distinction between conceptual and practical autonomy.',
                                 scope='summary', access_method='authorized_export')])
    answer = response(b)
    answer['candidate_parts'][0]['evidence'].append({
       'source_id': b['request']['sources'][1]['source_id'], 'quote':'between conceptual and practical autonomy'})
    assert len(validate_chatgpt_response(b, answer)['candidate_parts'][0]['evidence']) == 2


def test_duplicate_source_rejected():
    fail('CHATGPT_BUNDLE_INVALID', bundle, [source(),source()])


def test_bundle_tamper_rejected():
    b=bundle(); b['request']['sources'][0]['text'] = 'A changed source'
    fail('CHATGPT_BUNDLE_INTEGRITY', verify_bundle, b)


def test_bundle_prompt_tamper_rejected_even_with_recomputed_digest():
    from daat.util import json_digest
    b=bundle(); b['prompt']='Changed prompt'
    b['bundle_sha256']=json_digest({k:v for k,v in b.items() if k!='bundle_sha256'})
    fail('CHATGPT_BUNDLE_INTEGRITY', verify_bundle, b)


def test_unsupported_response_digest():
    b=bundle(); r=response(b);r['request_sha256']='0'*64
    fail('CHATGPT_RESPONSE_INVALID', validate_chatgpt_response, b, r)


def test_fabricated_quote_rejected():
    b=bundle()
    fail('CHATGPT_CITATION_INVALID', validate_chatgpt_response, b, response(b, 'the actual article proves an absolute truth'))


def test_other_source_quote_rejected():
    b=bundle()
    r=response(b);r['candidate_parts'][0]['evidence'][0]['source_id']='src-false'
    fail('CHATGPT_CITATION_INVALID', validate_chatgpt_response, b, r)


def test_no_citation_rejected():
    b=bundle();r=response(b);r['candidate_parts'][0]['evidence']=[]
    fail('CHATGPT_CITATION_INVALID', validate_chatgpt_response, b, r)


def test_canonical_id_rejected():
    b=bundle();r=response(b);r['candidate_parts'][0]['text']='This is KP1234 canonical'
    fail('CHATGPT_AUTHORITY_INVALID', validate_chatgpt_response, b, r)


def test_extra_authority_key_rejected():
    b=bundle();r=response(b);r['candidate_parts'][0]['canonical']=True
    fail('CHATGPT_AUTHORITY_INVALID', validate_chatgpt_response, b, r)


def test_unknown_field_rejected():
    b=bundle();r=response(b);r['invented_field']='wrong'
    fail('CHATGPT_RESPONSE_INVALID', validate_chatgpt_response, b, r)


def test_invalid_confidence_rejected():
    b=bundle();r=response(b);r['candidate_parts'][0]['confidence']=True
    fail('CHATGPT_RESPONSE_INVALID', validate_chatgpt_response, b, r)


def test_many_candidates_rejected():
    b=bundle();r=response(b);r['candidate_parts'] *= 31
    fail('CHATGPT_RESPONSE_INVALID', validate_chatgpt_response, b, r)


def test_empty_candidates_allow_unknowns_only():
    b=bundle();r=response(b);r['candidate_parts']=[]
    out=validate_chatgpt_response(b,r)
    assert out['candidate_parts']==[] and out['unknowns']


def test_cli_roundtrip(tmp_path):
    input_json=tmp_path/'input.json'; bundle_json=tmp_path/'bundle.json'; response_json=tmp_path/'response.json'; draft_json=tmp_path/'draft.json'
    input_json.write_text(json.dumps({'purpose':'Review research','sources':[source()]}),encoding='utf-8')
    def run(*argv):
        return subprocess.run([sys.executable, '-m', 'daat', *map(str, argv)], cwd=Path(__file__).parent.parent,
                              capture_output=True, text=True, timeout=12)
    denied=run('chatgpt-build-prompt', input_json, '--out', bundle_json)
    assert denied.returncode==2 and not bundle_json.exists()
    created=run('chatgpt-build-prompt', input_json, '--rights-acknowledged', '--allow-chatgpt-sharing', '--out', bundle_json)
    assert created.returncode==0, created.stderr
    b=json.loads(bundle_json.read_text(encoding='utf-8'))
    response_json.write_text(json.dumps(response(b)), encoding='utf-8')
    result=run('chatgpt-verify-response','--bundle',bundle_json,'--response',response_json,'--out',draft_json)
    assert result.returncode==0, result.stderr
    assert json.loads(draft_json.read_text(encoding='utf-8'))['status'].startswith('noncanonical')
    assert 'communication supports' not in result.stdout


def test_repair_prompt_is_bounded_and_reuses_exact_request():
    b=bundle()
    result=make_repair_prompt(b, 'CHATGPT_CITATION_INVALID')
    assert result.startswith(b['prompt'])
    assert b['request_sha256'] in result
    assert 'sous-chaînes EXACTES' in result
    fail('CHATGPT_REPAIR_UNSUPPORTED', make_repair_prompt, b, 'CHATGPT_BUNDLE_INVALID')

def test_url_query_with_authentication_token_rejected():
    fail('CHATGPT_INPUT_INVALID', bundle, [source(locator='https://medium.com/article?session_token=abc')])


def test_duplicate_candidate_rejected():
    b=bundle();r=response(b);r['candidate_parts'].append(copy.deepcopy(r['candidate_parts'][0]))
    fail('CHATGPT_RESPONSE_INVALID', validate_chatgpt_response, b, r)

def test_duplicate_citation_rejected():
    b=bundle();r=response(b);r['candidate_parts'][0]['evidence'] *= 2
    fail('CHATGPT_CITATION_INVALID', validate_chatgpt_response, b, r)

def test_deep_authority_payload_fails_closed():
    b=bundle();r=response(b)
    r['extra']=[[[[[[[[[[[[[['nested']]]]]]]]]]]]]]
    fail('CHATGPT_RESPONSE_INVALID', validate_chatgpt_response, b, r)

def test_unhashable_source_scope_fails_closed():
    fail('CHATGPT_INPUT_INVALID', bundle, [source(scope=['full_text'])])
