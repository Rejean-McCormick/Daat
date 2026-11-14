"""Host-injected, policy-gated external source PREVIEW port (no IK ingress).

The trusted host, never client JSON, supplies the authenticated actor, verified
provider grants, bounded connector and cryptographically verified output proof.
This module does not ship credentials, HTTP, DB drivers, a transport or source
catalogue. It has no ability to publish or build Kristals.
"""
from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Any, Mapping, Protocol

from .bridge import VerifiedPrincipal
from .catalog import source_family, LANES
from .candidates import deterministic_candidates
from .errors import AdmissionError
from .security import SecurityGate, PolicyRequest, PolicyAuthority, AuditSink
from .source import Evidence
from .util import json_digest, canonical_bytes

_REF = re.compile(r"^urn:[a-z0-9][a-z0-9_.-]{1,60}:[a-zA-Z0-9_:/#.%-]{2,850}$")
_ID = re.compile(r"^[a-z][a-z0-9_.-]{2,80}$")
_SHA = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class HostedSourceCall:
    admission_ref: str             # host-scoped identifier, NOT proof itself
    claimed_tenant: str
    claimed_system: str
    adapter_id: str
    source_ref: str                # stable opaque *source-owner* reference
    source_family_id: str
    source_revision: str
    purpose: str
    requested_count: int
    lane: str

    def __post_init__(self):
        if not _REF.fullmatch(self.source_ref):
            raise AdmissionError("SOURCE_REF_INVALID", "Only bounded opaque source-owner URNs are accepted")
        if not _ID.fullmatch(self.adapter_id) or not self.source_revision or len(self.source_revision) > 200:
            raise AdmissionError("SOURCE_REF_INVALID", "Pinned source revision and adapter required")
        if self.lane not in LANES:
            raise AdmissionError("SOURCE_LANE_INVALID", "Unknown declared access lane")
        if type(self.requested_count) is not int or not (1 <= self.requested_count <= 10000):
            raise AdmissionError("SOURCE_LIMIT_INVALID", "Invalid requested record count")
        if not self.purpose or len(self.purpose) > 250:
            raise AdmissionError("SOURCE_REF_INVALID", "Purpose required")
        source_family(self.source_family_id)


@dataclass(frozen=True)
class OwnerExtraction:
    records: tuple[Evidence, ...]
    owner_source_sha256: str
    producer_revision: str
    rights_ref: str
    warnings: tuple[str, ...] = ()


class HostedAuthenticator(Protocol):
    def verify(self, call: HostedSourceCall) -> VerifiedPrincipal: ...


class HostedSourceGrantVerifier(Protocol):
    def verify_grant(self, call: HostedSourceCall, principal: VerifiedPrincipal) -> bool: ...


class HostedReader(Protocol):
    def extract(self, call: HostedSourceCall, principal: VerifiedPrincipal) -> OwnerExtraction: ...


class HostedExtractionVerifier(Protocol):
    def verify(self, call: HostedSourceCall, result: OwnerExtraction,
               principal: VerifiedPrincipal) -> bool: ...


class HostedOnramp:
    MAX_EVIDENCE_BYTES = 2_000_000

    def __init__(self, *, authenticator: HostedAuthenticator | None = None,
                 source_grants: HostedSourceGrantVerifier | None = None,
                 output_verifier: HostedExtractionVerifier | None = None,
                 policy: PolicyAuthority | None = None, audit: AuditSink | None = None,
                 workers: Mapping[str, HostedReader] | None = None,
                 allowlist: Mapping[str, tuple[str, str]] | None = None):
        self.authenticator = authenticator
        self.source_grants = source_grants
        self.output_verifier = output_verifier
        self.security = SecurityGate(policy, audit)
        self.workers = dict(workers or {})
        # ID -> (approved lane, source family ID). Operator-controlled, never caller-defined.
        self.allowlist = dict(allowlist or {})

    def preview(self, call: HostedSourceCall) -> dict[str, Any]:
        if not all((self.authenticator, self.source_grants, self.output_verifier)):
            raise AdmissionError("AUTHENTICATION_UNCONFIGURED", "Trusted host identity, grant and extraction verification required")
        if call.adapter_id not in self.allowlist or call.adapter_id not in self.workers:
            raise AdmissionError("ADAPTER_UNAVAILABLE", "No approved host reader for adapter")
        if self.allowlist[call.adapter_id] != (call.lane, call.source_family_id):
            raise AdmissionError("ADAPTER_UNAVAILABLE", "Host adapter lane or family not allowed")
        principal = self.authenticator.verify(call)
        if not isinstance(principal, VerifiedPrincipal) or not principal.trusted or principal.audience != "daat":
            raise AdmissionError("AUTHENTICATION_FAILED", "Host principal not independently verified")
        if (principal.system != call.claimed_system or principal.tenant != call.claimed_tenant or
                not principal.actor or "daat-source-read" not in principal.capabilities):
            raise AdmissionError("AUTHORIZATION_DENIED", "Host caller/actor/tenant/capability mismatch")
        if not self.source_grants.verify_grant(call, principal):
            raise AdmissionError("SOURCE_UNTRUSTED", "Owner source access grant unavailable")
        intent = json_digest({"principal": principal.system, "tenant": principal.tenant,
                              "actor": principal.actor, "adapter": call.adapter_id,
                              "source_ref": call.source_ref, "revision": call.source_revision,
                              "lane": call.lane, "family": call.source_family_id,
                              "purpose": call.purpose, "records": call.requested_count})
        request = PolicyRequest(tenant=principal.tenant, caller=principal.system, actor=principal.actor,
                                action="daat.source.prepare", resource_owner="daat",
                                resource_class="source_preview", resource_selector=call.source_ref,
                                intent_digest=intent, requested_count=call.requested_count,
                                purpose=call.purpose, auth_assurance=principal.auth_assurance,
                                auth_age_seconds=principal.auth_age_seconds)
        decision = self.security.authorize(request)
        try:
            result = self.workers[call.adapter_id].extract(call, principal)
            if not isinstance(result, OwnerExtraction):
                raise AdmissionError("SOURCE_OUTPUT_INVALID", "Worker did not return typed owner extraction")
            if result.producer_revision != call.source_revision or not _SHA.fullmatch(result.owner_source_sha256):
                raise AdmissionError("SOURCE_INTEGRITY", "Worker source revision/hash mismatch")
            if not result.rights_ref or len(result.rights_ref) > 200:
                raise AdmissionError("SOURCE_RIGHTS_INVALID", "Owner rights reference missing")
            if len(result.records) > call.requested_count:
                raise AdmissionError("SOURCE_LIMIT", "Reader emitted more rows than authorized")
            if not self.output_verifier.verify(call, result, principal):
                raise AdmissionError("SOURCE_INTEGRITY", "Host cannot verify produced extraction")
            extracted = [record.as_dict() for record in result.records]
            if len(canonical_bytes(extracted)) > self.MAX_EVIDENCE_BYTES:
                raise AdmissionError("SOURCE_LIMIT", "Extracted evidence exceeds hosted preview size")
            data = {
                "format": "daat.local-evidence-preview/0.1.0-prototype",
                "authority": "noncanonical_unreviewed",
                "owner_handoff": "blocked_pending_owner_adopted_contract",
                "source": {"kind": "hosted_" + call.lane, "family_id": call.source_family_id,
                           "remote_ref": call.source_ref, "revision": call.source_revision,
                           "manifest_sha256": result.owner_source_sha256,
                           "rights": {"verification": "trusted_host_grant_verifier",
                                      "rights_ref": result.rights_ref, "tenant": principal.tenant,
                                      "purpose": call.purpose}},
                "extraction": {"adapter_id": call.adapter_id, "adapter_version": "host_pinned",
                               "deterministic": None, "executed_external_code": "trusted_worker_only"},
                "records": extracted,
                "warnings": list(result.warnings),
                "policy_decision_reference": decision.decision_id,
            }
            data["candidates"] = deterministic_candidates(data)
            data["preview_sha256"] = json_digest(data)
            self.security.emit("prepared", decision, request, "success")
            return data
        except Exception:
            # The worker may have performed a *read*, never an owner mutation; audit failure remains fatal.
            self.security.emit("preparation_failed", decision, request, "failed")
            raise
