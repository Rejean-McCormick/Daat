"""Opt-in bounded HTTPS reader for publicly documented, host-approved endpoints.

No browser login, cookie copying, paywall bypass, automatic cross-host redirect,
or external owner contract adoption. Host networking remains independently gated.
"""
from __future__ import annotations
import http.client
import ipaddress
import json
import socket
import ssl
from urllib.parse import urlsplit
from dataclasses import dataclass
from typing import Protocol

from .model import BridgeError, Limits

class Transport(Protocol):
    def get(self,url:str,*,headers:dict[str,str]|None=None)->tuple[int,dict[str,str],bytes]: ...

@dataclass(frozen=True)
class RemotePolicy:
    allow_hosts: tuple[str,...] = ()
    explicit_network_consent: bool = False
    max_bytes: int = 2_000_000
    timeout_seconds: int = 12
    
    def __post_init__(self):
        if self.max_bytes < 1 or self.max_bytes > 10_000_000 or not 1 <= self.timeout_seconds <= 60:
            raise BridgeError('NETWORK_POLICY','Unsafe network bounds')
        if any(not host or host.lower()!=host or '/' in host or ':' in host for host in self.allow_hosts):
            raise BridgeError('NETWORK_POLICY','Only explicit DNS hostnames may be allowlisted')

def check_url(url:str,policy:RemotePolicy)->tuple[str,str]:
    try: parts=urlsplit(url)
    except ValueError as exc: raise BridgeError('NETWORK_URL','Invalid URL') from exc
    if (not policy.explicit_network_consent or parts.scheme!='https' or not parts.hostname or
            parts.port not in (None,443) or parts.username or parts.password or
            parts.fragment or parts.hostname.lower() not in policy.allow_hosts):
        raise BridgeError('NETWORK_DENIED','HTTPS source host not explicitly approved')
    try: ipaddress.ip_address(parts.hostname)
    except ValueError: pass
    else: raise BridgeError('NETWORK_DENIED','IP address literals disallowed')
    if len(url)>3000 or any(c in url for c in ('\r','\n','\x00')):
        raise BridgeError('NETWORK_URL','URL is unbounded')
    path=parts.path or '/'
    if parts.query:
        query=parts.query.lower()
        if any(s in query for s in ('api_key=', 'apikey=', 'password=', 'token=', 'access_key=', 'secret=', 'session=')):
            raise BridgeError('NETWORK_SECRET','Credential in URL query disallowed')
        path+='?'+parts.query
    return parts.hostname,path

def public_ip(host:str)->str:
    try: infos=socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
    except OSError as exc: raise BridgeError('NETWORK_DNS','DNS resolution failed') from exc
    vetted=[]
    for family,_,_,_,address in infos:
        ip=ipaddress.ip_address(address[0])
        if not ip.is_global:
            raise BridgeError('NETWORK_SSRF','Non-public DNS answer rejected')
        vetted.append(str(ip))
    if not vetted: raise BridgeError('NETWORK_DNS','No address')
    return vetted[0]

class _PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self,host:str,ip:str,timeout:int):
        super().__init__(host,443,timeout=timeout,context=ssl.create_default_context())
        self.ip=ip
    def connect(self):
        # Connect to the vetted DNS address while verifying original TLS hostname.
        sock=socket.create_connection((self.ip,443),timeout=self.timeout)
        self.sock=self._context.wrap_socket(sock,server_hostname=self.host)

class BoundedHTTPS:
    def __init__(self,policy:RemotePolicy): self.policy=policy
    def get(self,url:str,*,headers:dict[str,str]|None=None)->tuple[int,dict[str,str],bytes]:
        host,path=check_url(url,self.policy)
        ip=public_ip(host)
        headers=dict(headers or {})
        for k,v in headers.items():
            if (k.lower() in {'host','cookie','proxy-authorization','connection','transfer-encoding'} or
                    '\r' in k+v or '\n' in k+v):
                raise BridgeError('NETWORK_HEADER','Unsafe request header')
        headers['User-Agent']='DaaT-Information-Bridge/1.0 (approved-collection-only)'
        headers['Accept-Encoding']='identity'
        connection=_PinnedHTTPS(host,ip,self.policy.timeout_seconds)
        try:
            connection.request('GET',path,headers=headers)
            response=connection.getresponse()
            status=response.status
            hdrs={k.lower():v for k,v in response.getheaders()}
            if status in (301,302,303,307,308):
                raise BridgeError('NETWORK_REDIRECT','Redirect not automatically followed; re-evaluate provider/rights')
            if status in (401,403): raise BridgeError('NETWORK_AUTH','Provider denied access')
            if status==429: raise BridgeError('NETWORK_RATE_LIMIT','Provider rate limit; host must schedule later')
            if status>=500: raise BridgeError('NETWORK_PROVIDER','Provider unavailable')
            if status not in (200,204,206,304):
                raise BridgeError('NETWORK_HTTP',f'Provider response status {status}')
            if hdrs.get('content-encoding','identity').lower() not in ('identity',''):
                raise BridgeError('NETWORK_ENCODING','Compressed response not permitted by bounded reader')
            if int(hdrs.get('content-length','0') or '0')>self.policy.max_bytes:
                raise BridgeError('NETWORK_LIMIT','Content-Length over cap')
            payload=response.read(self.policy.max_bytes+1)
            if len(payload)>self.policy.max_bytes:
                raise BridgeError('NETWORK_LIMIT','Body over cap')
            return status,hdrs,payload
        except (OSError,http.client.HTTPException,ssl.SSLError,ValueError) as exc:
            raise BridgeError('NETWORK_TRANSPORT','Connection failed or invalid response') from exc
        finally:
            connection.close()


def get_paginated_json(client:Transport,initial_url:str,*,max_pages:int=5,
                       max_records:int=200,headers:dict[str,str]|None=None)->tuple[list[dict],list[dict]]:
    """JSON REST pagination for explicitly vetted same-host next links, no inference of content rights."""
    if not 1<=max_pages<=50 or not 1<=max_records<=5000:
        raise BridgeError('NETWORK_LIMIT','Unsafe pagination bounds')
    host=urlsplit(initial_url).hostname
    pageurl=initial_url; seen=set(); records=[]; history=[]
    for _ in range(max_pages):
        if pageurl in seen: raise BridgeError('PAGINATION_LOOP','Repeated page')
        if urlsplit(pageurl).hostname!=host or urlsplit(pageurl).scheme!='https':
            raise BridgeError('PAGINATION_HOST','Cross-host next page blocked')
        seen.add(pageurl)
        status,hdr,payload=client.get(pageurl,headers=headers)
        if status==304:
            history.append({'url':pageurl,'status':304,'etag':hdr.get('etag','')})
            break
        if status in (204,):break
        if len(payload)>5_000_000: raise BridgeError('NETWORK_LIMIT','Page exceeds limit')
        try: data=json.loads(payload)
        except (ValueError,UnicodeDecodeError) as exc:
            raise BridgeError('NETWORK_JSON','JSON parse error') from exc
        if isinstance(data,list): items=data; nxt=None
        elif isinstance(data,dict):
            items=data.get('items',data.get('results',data.get('data',[])))
            nxt=data.get('next') or data.get('next_url')
            # Never invent provider-specific cursor protocols.
        else: raise BridgeError('NETWORK_JSON','Unsupported response shape')
        if not isinstance(items,list) or any(not isinstance(x,dict) for x in items):
            raise BridgeError('NETWORK_JSON','Expected list of records')
        if len(records)+len(items)>max_records:
            raise BridgeError('NETWORK_LIMIT','Total record cap')
        records+=items
        history.append({'url':pageurl,'status':status,'etag':hdr.get('etag',''),
                        'last_modified':hdr.get('last-modified',''),'items':len(items)})
        if not nxt: break
        if not isinstance(nxt,str) or not nxt.startswith('https://'):
            raise BridgeError('PAGINATION_LINK','Provider next URL must be explicit HTTPS URL')
        pageurl=nxt
    else:
        if nxt:
            history.append({'incomplete':True,'reason':'max_pages'})
    return records,history
