"""Bounded OOXML/OpenDocument/ePub text extraction with provenance locators.

These parsers are best-effort extracts, never faithful visual renders or office
macro execution. Complex/untrusted office files require owner isolation.
"""
from __future__ import annotations
from io import BytesIO
from pathlib import PurePosixPath
import re
import stat
import zipfile
from typing import Iterable

from .model import BridgeError, Limits
from .ingest import xml_safe, local_name, html_text


def _members(blob:bytes,limits:Limits)->dict[str,bytes]:
    if len(blob)>limits.max_file_bytes:raise BridgeError('OFFICE_LIMIT','Compressed document cap')
    try: archive=zipfile.ZipFile(BytesIO(blob))
    except zipfile.BadZipFile as exc:raise BridgeError('OFFICE_INVALID','Not a valid office archive') from exc
    result={};total=0
    with archive:
        infos=archive.infolist()
        if len(infos)>limits.max_files:raise BridgeError('OFFICE_LIMIT','Too many parts')
        for info in infos:
            if info.is_dir():continue
            path=PurePosixPath(info.filename)
            if info.filename.startswith('/') or '..' in path.parts or '\\' in info.filename or\
               stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1 or info.filename in result:
                raise BridgeError('OFFICE_UNSAFE','Unsafe archive member')
            total+=info.file_size
            if total>limits.max_file_bytes or info.file_size>limits.max_archive_ratio*max(1,info.compress_size):
                raise BridgeError('OFFICE_LIMIT','Decompression budget exceeded')
            if info.filename.endswith(('.xml','.rels','.xhtml','.html','.opf')):
                with archive.open(info) as stream:
                    payload=stream.read(info.file_size+1)
                if len(payload)!=info.file_size:raise BridgeError('OFFICE_INVALID','Part size mismatch')
                result[info.filename]=payload
    return result


def read_office(blob:bytes,suffix:str,limits:Limits)->list[tuple[str,str]]:
    parts=_members(blob,limits)
    records=[]
    if suffix=='.docx':
        names=['word/document.xml']
    elif suffix=='.pptx':
        names=sorted((p for p in parts if re.fullmatch(r'ppt/slides/slide\d+\.xml',p)),
                     key=lambda p:int(re.search(r'slide(\d+)',p).group(1)))
    elif suffix=='.odt':
        names=['content.xml']
    elif suffix=='.epub':
        names=sorted(p for p in parts if p.lower().endswith(('.xhtml','.html')))
    elif suffix=='.xlsx':
        names=sorted(p for p in parts if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',p))
        shared=[]
        if 'xl/sharedStrings.xml' in parts:
            sharedroot=xml_safe(parts['xl/sharedStrings.xml'])
            for si in (x for x in sharedroot.iter() if local_name(x.tag)=='si'):
                shared.append(''.join((n.text or '') for n in si.iter() if local_name(n.tag)=='t'))
    else:raise BridgeError('OFFICE_FORMAT','Unsupported office type')
    if not names or any(n not in parts for n in names):
        raise BridgeError('OFFICE_INVALID','Expected text part missing')
    for name in names:
        if suffix=='.epub':
            text=html_text(parts[name].decode('utf-8-sig'))
            if text:records.append((name,text))
            continue
        root=xml_safe(parts[name])
        if suffix=='.xlsx':
            for row in (r for r in root.iter() if local_name(r.tag)=='row'):
                cells=[]
                for cell in (c for c in row if local_name(c.tag)=='c'):
                    value=next(((v.text or '') for v in cell if local_name(v.tag)=='v'),'')
                    inline=next((x for x in cell if local_name(x.tag)=='is'),None)
                    if inline is not None:
                        value=''.join((t.text or '') for t in inline.iter() if local_name(t.tag)=='t')
                    if cell.attrib.get('t')=='s':
                        try:value=shared[int(value)]
                        except (IndexError,ValueError):raise BridgeError('OFFICE_INVALID','Invalid shared string index')
                    has_formula=any(local_name(x.tag)=='f' for x in cell)
                    if has_formula:
                        value='[formula-not-executed] cached-value='+value
                    cells.append(f"{cell.attrib.get('r','cell')}={value}")
                if cells:records.append((f'{name}#row:{row.attrib.get("r", "unknown")}', '\t'.join(cells)))
        elif suffix=='.odt':
            for i,node in enumerate((n for n in root.iter() if local_name(n.tag) in ('p','h')),1):
                text=''.join(n.text or '' for n in node.iter() if n.text).strip()
                if text:records.append((f'{name}#para:{i}',text))
        else:
            buffer=[]
            for node in root.iter():
                if local_name(node.tag)=='t' and node.text:
                    buffer.append(node.text)
                elif local_name(node.tag) in ('p','br'):
                    buffer.append('\n')
            text=''.join(buffer).strip()
            if text:records.append((name,text))
        if len(records)>limits.max_items:
            raise BridgeError('OFFICE_LIMIT','Too many extracted segments')
    if sum(len(text) for _,text in records)>limits.max_total_chars:
        raise BridgeError('OFFICE_LIMIT','Text extraction too large')
    return records
