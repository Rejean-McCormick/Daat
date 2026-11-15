"""Explicit source rights and loss-aware local information model.

No implicit rights, AI authority or Kristal semantics. The strings are a DaaT
internal draft, NOT owner IK/Konfid/Mediatheque wire messages.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any

RIGHTS = ('read', 'copy', 'retain', 'transform', 'ai_disclosure')
CONTENT_KINDS = ('reference_only', 'abstract', 'excerpt', 'full_text_authorized',
                 'dataset', 'structured_record', 'media_derivative')

class BridgeError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f'{code}: {message}')
        self.code = code


def digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')


def timestamp(value: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (TypeError, ValueError, AttributeError) as exc:
        raise BridgeError('DATE_INVALID', 'Expected an offset-aware ISO timestamp') from exc
    if dt.tzinfo is None:
        raise BridgeError('DATE_INVALID', 'Naive timestamp is forbidden')
    return dt.astimezone(timezone.utc)

@dataclass(frozen=True)
class Limits:
    max_file_bytes: int = 15_000_000
    max_items: int = 2500
    max_total_chars: int = 2_000_000
    max_fragment_chars: int = 5000
    max_context_chars: int = 70_000
    max_files: int = 500
    max_archive_ratio: int = 50
    max_pages: int = 20

    def __post_init__(self):
        for key, val in vars(self).items():
            if type(val) is not int or val < 1 or val > 50_000_000:
                raise BridgeError('LIMIT_INVALID', f'Invalid limit: {key}')
        if self.max_fragment_chars > self.max_total_chars:
            raise BridgeError('LIMIT_INVALID', 'Fragment bound exceeds total bound')

@dataclass(frozen=True)
class Rights:
    """Rights evidence must be explicitly supplied. Never inferred from login or HTTP 200."""
    read: str = 'unknown'
    copy: str = 'unknown'
    retain: str = 'unknown'
    transform: str = 'unknown'
    ai_disclosure: str = 'unknown'
    basis: str = ''
    evidence_ref: str = ''
    checked_at: str = field(default_factory=utcnow)
    expires_at: str | None = None
    attestation: str = 'unverified'  # operator_asserted | host_verified | unverified
    classification: str = 'internal'
    tenant: str = 'local'
    purpose: str = 'context_preparation'
    revoked: bool = False

    def __post_init__(self):
        if any(getattr(self, k) not in {'allowed','denied','unknown'} for k in RIGHTS):
            raise BridgeError('RIGHTS_INVALID', 'Every permission must be allowed/denied/unknown')
        if self.attestation not in {'unverified','operator_asserted','host_verified'}:
            raise BridgeError('RIGHTS_INVALID', 'Unknown attestation')
        if self.classification not in {'public','internal','confidential','restricted'}:
            raise BridgeError('RIGHTS_INVALID', 'Unknown classification')
        if not self.tenant or len(self.tenant) > 128 or not self.purpose or len(self.purpose) > 200:
            raise BridgeError('RIGHTS_INVALID','Tenant and purpose must be bounded')
        timestamp(self.checked_at)
        if self.expires_at is not None:
            timestamp(self.expires_at)
        if any(getattr(self, k) == 'allowed' for k in RIGHTS) and (not self.basis.strip() or not self.evidence_ref.strip()):
            raise BridgeError('RIGHTS_INVALID', 'Allowed rights require explicit basis and non-secret evidence reference')
        if any(x in (self.basis + self.evidence_ref).lower() for x in ('bearer ', 'password=', 'api_key=', 'token=')):
            raise BridgeError('SECRET_REFERENCE', 'Rights evidence appears to include a credential')

    def allowed(self, action: str, *, now: datetime | None = None, target: str='manual_chatgpt') -> bool:
        if action not in RIGHTS:
            raise BridgeError('RIGHTS_INVALID', 'Unknown action')
        current = now or datetime.now(timezone.utc)
        if self.revoked or (self.expires_at is not None and timestamp(self.expires_at) <= current):
            return False
        if getattr(self, action) != 'allowed' or self.attestation == 'unverified':
            return False
        if action == 'ai_disclosure' and target != 'manual_chatgpt' and self.attestation != 'host_verified':
            return False
        return True

    def can_export_text(self, target: str='manual_chatgpt') -> bool:
        return all(self.allowed(action, target=target) for action in RIGHTS)

    def policy(self) -> dict[str,str]:
        return {k: getattr(self, k) for k in RIGHTS}

@dataclass(frozen=True)
class SourceItem:
    platform_id: str
    external_id: str
    revision: str
    content_kind: str
    rights: Rights
    title: str = ''
    author: str = ''
    url: str = ''
    acquired_via: str = 'user_paste'
    observed_at: str = field(default_factory=utcnow)
    language: str = 'und'
    source_ref: str = ''

    def __post_init__(self):
        if self.content_kind not in CONTENT_KINDS:
            raise BridgeError('SOURCE_KIND', 'Unknown content kind')
        for k in ('platform_id','external_id','revision'):
            val = getattr(self,k)
            if not isinstance(val,str) or not val.strip() or len(val) > 1200 or '\x00' in val:
                raise BridgeError('SOURCE_INVALID', f'Invalid {k}')
        timestamp(self.observed_at)
        if self.source_ref and not self.source_ref.startswith('src-'):
            raise BridgeError('SOURCE_INVALID', 'Source reference must use local src- namespace')

    def ref(self) -> str:
        return self.source_ref or 'src-' + digest((self.rights.tenant, self.platform_id,
                                                  self.external_id,self.revision))[:24]

@dataclass(frozen=True)
class Fragment:
    source_ref: str
    source_revision: str
    text: str
    locator: str
    content_kind: str
    transformation: str = 'extract-v1'
    quote_verified: bool = False
    warning: str = ''
    fragment_id: str = ''

    def __post_init__(self):
        if self.content_kind not in CONTENT_KINDS or self.content_kind == 'reference_only':
            raise BridgeError('FRAGMENT_INVALID', 'Fragment must reflect obtained content, not reference_only')
        if not isinstance(self.text, str) or not self.text.strip() or len(self.text) > 2_000_000:
            raise BridgeError('FRAGMENT_INVALID', 'Text absent or unbounded')
        if not self.locator or len(self.locator) > 1200:
            raise BridgeError('FRAGMENT_INVALID', 'Anchor locator required')

    def ident(self) -> str:
        return self.fragment_id or 'frag-' + digest((self.source_ref, self.source_revision,
                                   self.locator, sha_text(self.text)))[:24]
