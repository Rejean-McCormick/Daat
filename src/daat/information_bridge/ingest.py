"""Bounded, offline authorized ingestion with exact source provenance.

Network calls are separate from the parsers. Never read a connected account,
copy a browser session, execute documents, or acquire a remote page here.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from io import BytesIO
import csv
import hashlib
import io
import json
import re
import stat
import zipfile
import xml.etree.ElementTree as ET
from typing import Any

from .model import BridgeError, Fragment, SourceItem, Rights, Limits, digest, sha_text
from ..source import ReadLimits, confined_path
from ..connectors.common import parse_tabular, json_strict, decode_utf8
from ..connectors.bibliography import read_bibliography
from ..connectors.pdf import read_pdf
from ..connectors.git import read_git
from ..errors import AdmissionError

_TEXT = {'.txt', '.md', '.rst', '.html', '.htm', '.xml', '.rss', '.atom'}
_TABULAR = {'.csv', '.tsv', '.json', '.jsonl'}
_BIBLIO = {'.ris', '.bib'}
_ACCEPT = _TEXT | _TABULAR | _BIBLIO | {'.pdf','.zip','.docx','.xlsx','.pptx','.odt','.epub','.eml'}

class _TextHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.hidden = 0
        self.links: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag in {'script','style','noscript','svg','template','iframe','form'}:
            self.hidden += 1
        if tag in {'p','li','h1','h2','h3','h4','article','section','div','br'}:
            self.text.append('\n')
    def handle_endtag(self, tag):
        if tag in {'script','style','noscript','svg','template','iframe','form'} and self.hidden:
            self.hidden -= 1
        if tag in {'p','li','h1','h2','h3','h4','article','section'}:
            self.text.append('\n')
    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)

def html_text(text: str) -> str:
    # Best-effort text extraction, NOT an HTML sanitizer for display in a browser.
    if '<!DOCTYPE' in text.upper() and ('SYSTEM' in text.upper() or 'PUBLIC' in text.upper()):
        raise BridgeError('HTML_UNSAFE','External document declarations not accepted')
    parser = _TextHTML()
    parser.feed(text)
    return re.sub(r'\n{3,}', '\n\n', ''.join(parser.text)).strip()

def xml_safe(blob: bytes) -> ET.Element:
    head = blob[:8192].upper()
    if b'<!DOCTYPE' in head or b'<!ENTITY' in head:
        raise BridgeError('XML_UNSAFE','DTD and XML entities refused')
    try:
        return ET.fromstring(blob)
    except ET.ParseError as exc:
        raise BridgeError('XML_INVALID', 'Malformed XML') from exc

def local_name(name: str) -> str:
    return name.rsplit('}',1)[-1].lower()

@dataclass
class PreparedCorpus:
    sources: list[SourceItem] = field(default_factory=list)
    fragments: list[Fragment] = field(default_factory=list)
    records: list[dict[str,Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    def add(self, source: SourceItem, fragments: list[Fragment], records: list[dict[str,Any]]|None = None):
        if any(x.ref() == source.ref() for x in self.sources):
            raise BridgeError('DUPLICATE_SOURCE','Exact source revision was already included')
        self.sources.append(source)
        self.fragments.extend(fragments)
        self.records.extend(records or [])

class LocalIngestor:
    def __init__(self, *, limits: Limits|None=None):
        self.limits = limits or Limits()
        self.corpus = PreparedCorpus()

    def _validate(self, source: SourceItem):
        for permission in ('read','copy','transform'):
            if not source.rights.allowed(permission):
                raise BridgeError('SOURCE_USE_NOT_AUTHORIZED',
                    'Source parsing requires explicit unexpired read/copy/transform permissions')
        if len(self.corpus.sources) >= self.limits.max_items:
            raise BridgeError('LIMIT','Source count limit')

    def _segments(self, text: str, source: SourceItem, label: str, *, is_original: bool=True) -> list[Fragment]:
        if not text.strip():
            return []
        if len(text) > self.limits.max_total_chars:
            raise BridgeError('LIMIT','Text over corpus limit')
        chunk = self.limits.max_fragment_chars
        # Exact, contiguous segments with deterministic character-offset anchors.
        segments = []
        for start in range(0,len(text),chunk):
            part = text[start:start+chunk]
            if part.strip():
                segments.append(Fragment(source_ref=source.ref(),source_revision=source.revision,
                       text=part, locator=f'{label}#char:{start}-{start+len(part)}',
                       content_kind=source.content_kind, quote_verified=is_original,
                       transformation='direct-text-v1' if is_original else 'derived-extract-v1'))
        return segments

    def add_text(self, *, source:SourceItem, text:str, locator:str='user-paste', quote_verified:bool=True):
        self._validate(source)
        if source.content_kind == 'reference_only':
            if text.strip():
                raise BridgeError('SCOPE_INVALID','Reference-only source cannot carry article text')
            frags = []
        else:
            frags = self._segments(text,source,locator,is_original=quote_verified)
        if sum(len(f.text) for f in self.corpus.fragments)+sum(len(f.text) for f in frags)>self.limits.max_total_chars:
            raise BridgeError('LIMIT','Cumulative text limit exceeded')
        self.corpus.add(source,frags)
        return len(frags)

    def add_reference(self, source:SourceItem):
        # An operator-supplied identifier may be remembered as a non-retrieved
        # reference even when remote reading/copying rights are unknown.
        if len(self.corpus.sources)>=self.limits.max_items:
            raise BridgeError('LIMIT','Reference count cap reached')
        if source.content_kind != 'reference_only':
            raise BridgeError('SCOPE_INVALID','Reference requires reference_only kind')
        self.corpus.add(source,[])

    def add_file(self, *, root:Path, relative_path:str, source:SourceItem, git_commit:str|None=None):
        self._validate(source)
        if source.content_kind == 'reference_only':
            raise BridgeError('SCOPE_INVALID','File content cannot be represented as reference_only')
        try:
            path=confined_path(root,relative_path,allow_directory=git_commit is not None)
        except AdmissionError as exc:
            raise BridgeError('FILE_UNSAFE',str(exc)) from exc
        limits=ReadLimits(max_source_bytes=self.limits.max_file_bytes,
                max_records=min(10000,self.limits.max_items),max_text_chars=min(1_000_000,self.limits.max_total_chars),
                max_files=self.limits.max_files,max_archive_ratio=self.limits.max_archive_ratio)
        frags: list[Fragment]=[]
        records: list[dict[str,Any]]=[]
        if git_commit:
            try:
                evs,_,warnings,_=read_git(path,git_commit,limits,source.ref())
            except AdmissionError as exc:
                raise BridgeError('GIT_REJECTED',str(exc)) from exc
            self.corpus.warnings.extend(warnings)
            for e in evs:
                text = str(e.data.get('text',''))
                frags.extend(self._segments(text,source,e.location,is_original=True))
        else:
            if not path.is_file() or path.stat().st_size > self.limits.max_file_bytes:
                raise BridgeError('LIMIT','Regular bounded file required')
            suffix=path.suffix.lower()
            if suffix not in _ACCEPT:
                raise BridgeError('FORMAT_UNSUPPORTED','Unsupported source format')
            if source.content_kind=='full_text_authorized' and suffix in _TABULAR | _BIBLIO | {'.xml','.rss','.atom'}:
                raise BridgeError('SCOPE_INVALID','Bibliography/tabular/feed files cannot imply full article')
            if suffix in {'.docx','.xlsx','.pptx','.odt','.epub'}:
                from .office import read_office
                if suffix=='.xlsx' and source.content_kind!='structured_record':
                    raise BridgeError('SCOPE_INVALID','Spreadsheet values must remain structured records')
                for locator,text in read_office(path.read_bytes(),suffix,self.limits):
                    frags.extend(self._segments(text,source,relative_path+'#'+locator,is_original=False))
            elif suffix=='.eml':
                from email import policy
                from email.parser import BytesParser
                mail=BytesParser(policy=policy.default).parsebytes(path.read_bytes())
                if mail.defects:raise BridgeError('EMAIL_INVALID','Malformed MIME message')
                parts=mail.walk() if mail.is_multipart() else (mail,)
                for i,part in enumerate(parts):
                    if part.get_content_disposition()=='attachment':continue
                    if part.get_content_type() not in ('text/plain','text/html'):continue
                    text=part.get_content()
                    if not isinstance(text,str):continue
                    if part.get_content_type()=='text/html':text=html_text(text)
                    frags.extend(self._segments(text,source,f'{relative_path}#mime:{i}',is_original=part.get_content_type()=='text/plain'))
            elif suffix == '.zip':
                frags, records = self._zip(path.read_bytes(),source,relative_path)
            elif suffix in _TABULAR:
                blob=path.read_bytes()
                try:
                    rows=parse_tabular(blob,suffix,limits)
                except AdmissionError as exc:
                    raise BridgeError('TABULAR_INVALID',str(exc)) from exc
                for anchor,row in rows:
                    raw=json.dumps(row,ensure_ascii=False,sort_keys=True,allow_nan=False)
                    frags.extend(self._segments(raw,source,f'{relative_path}#{anchor}',is_original=False))
                    records.append({'source_ref':source.ref(),'locator':anchor,'type':'structured_record',
                                    'sha256':sha_text(raw),'transform':'typed-json-v1'})
            elif suffix in _BIBLIO:
                if suffix == '.bib':
                    raise BridgeError('FORMAT_UNSUPPORTED','BibTeX requires approved parser; use RIS/JSON export')
                try:
                    evs,_,warnings=read_bibliography(path,limits,source.ref())
                except AdmissionError as exc:
                    raise BridgeError('BIBLIO_INVALID',str(exc)) from exc
                self.corpus.warnings.extend(warnings)
                for e in evs:
                    raw=json.dumps(e.data,ensure_ascii=False,sort_keys=True)
                    frags.extend(self._segments(raw,source,e.location,is_original=False))
            elif suffix == '.pdf':
                try:
                    evs,_=read_pdf(path,limits,source.ref())
                except AdmissionError as exc:
                    raise BridgeError('PDF_REJECTED',str(exc)) from exc
                for e in evs:
                    self.corpus.warnings.extend(e.warnings)
                    frags.extend(self._segments(str(e.data.get('text','')),source,e.location,is_original=False))
            elif suffix in ('.xml','.rss','.atom'):
                frags=self._xml(path.read_bytes(),source,relative_path)
            else:
                text=decode_utf8(path.read_bytes())
                if suffix in ('.html','.htm'):
                    text=html_text(text)
                frags=self._segments(text,source,relative_path,is_original=suffix not in ('.html','.htm'))
        if len(self.corpus.fragments)+len(frags) > self.limits.max_items*20:
            raise BridgeError('LIMIT','Fragment count limit exceeded')
        if sum(len(f.text) for f in self.corpus.fragments) + sum(len(f.text) for f in frags)>self.limits.max_total_chars:
            raise BridgeError('LIMIT','Cumulative text limit exceeded')
        self.corpus.add(source,frags,records)
        return len(frags)

    def _xml(self,blob:bytes,source:SourceItem,label:str) -> list[Fragment]:
        root=xml_safe(blob)
        nodes=[x for x in root.iter() if local_name(x.tag) in ('item','entry','record')]
        if len(nodes)>self.limits.max_items:
            raise BridgeError('LIMIT','XML node cap')
        result=[]
        for ix,node in enumerate(nodes):
            title=''; abstract=''; identifier=''
            for field in node.iter():
                key=local_name(field.tag)
                val=(field.text or '').strip()
                if len(val)>self.limits.max_fragment_chars:
                    val=val[:self.limits.max_fragment_chars]
                    self.corpus.warnings.append('xml_field_truncated')
                if key in ('title','name'): title=val or title
                if key in ('description','summary','abstract'): abstract=val or abstract
                if key in ('link','identifier','id'): identifier=val or identifier
            # Feed description is at most an abstract/excerpt, never asserted full article.
            raw=json.dumps({'title':title,'description_or_abstract':abstract,'identifier':identifier},ensure_ascii=False)
            if source.content_kind == 'full_text_authorized':
                raise BridgeError('SCOPE_INVALID','RSS/OAI records cannot imply full article')
            if source.content_kind == 'reference_only':
                continue
            result.extend(self._segments(raw,source,f'{label}#record:{ix+1}',is_original=False))
        return result

    def _zip(self,blob:bytes,source:SourceItem,label:str)->tuple[list[Fragment],list[dict]]:
        frags=[]; records=[]; total=0; names=set()
        try:
            z=zipfile.ZipFile(BytesIO(blob))
        except zipfile.BadZipFile as exc:
            raise BridgeError('ZIP_INVALID','Malformed ZIP') from exc
        with z:
            members=z.infolist()
            if len(members)>self.limits.max_files:
                raise BridgeError('LIMIT','Too many ZIP entries')
            for info in members:
                if info.is_dir():continue
                name=info.filename
                parts=PurePosixPath(name)
                if (not name or name.startswith('/') or '\\' in name or '..' in parts.parts or
                        name in names or stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1):
                    raise BridgeError('ZIP_UNSAFE','Unsafe archive entry')
                names.add(name)
                if info.file_size>self.limits.max_file_bytes or info.file_size > self.limits.max_archive_ratio*max(1,info.compress_size):
                    raise BridgeError('ZIP_BOMB','Unsafe compression or member size')
                total+=info.file_size
                if total > self.limits.max_file_bytes:
                    raise BridgeError('LIMIT','Uncompressed ZIP budget exceeded')
                if parts.suffix.lower() not in _TEXT | _TABULAR | {'.pdf'}:
                    self.corpus.warnings.append('zip_member_unsupported:'+name)
                    continue
                with z.open(info) as f:
                    payload=f.read(info.file_size+1)
                if len(payload)!=info.file_size:
                    raise BridgeError('ZIP_INVALID','Member changed size')
                suffix=parts.suffix.lower()
                if suffix=='.pdf':
                    # Avoid recursively re-parsing untrusted PDF inside ZIP in this port.
                    self.corpus.warnings.append('zip_pdf_requires_separate_sandbox:'+name)
                    continue
                if suffix in _TABULAR:
                    try: rows=parse_tabular(payload,suffix,ReadLimits(max_source_bytes=self.limits.max_file_bytes,
                       max_records=self.limits.max_items,max_text_chars=self.limits.max_fragment_chars*10),)
                    except AdmissionError as exc:
                        raise BridgeError('ZIP_TABULAR_INVALID',str(exc)) from exc
                    for anchor,row in rows:
                        raw=json.dumps(row,ensure_ascii=False,sort_keys=True)
                        frags.extend(self._segments(raw,source,label+'#'+name+'#'+anchor,is_original=False))
                        records.append({'source_ref':source.ref(),'locator':label+'#'+name+'#'+anchor,
                                        'type':'structured_record','sha256':sha_text(raw),'transform':'zip-json-v1'})
                else:
                    text=decode_utf8(payload)
                    if suffix in {'.htm','.html'}:
                        text=html_text(text)
                    frags.extend(self._segments(text,source,label+'#'+name,is_original=suffix not in {'.htm','.html'}))
        return frags,records
