from __future__ import annotations
from datetime import datetime, timedelta, timezone
import pytest

from daat.bridge import VerifiedPrincipal
from daat.errors import AdmissionError
from daat.hosted import HostedOnramp, HostedSourceCall, OwnerExtraction
from daat.security import BoundDecision
from daat.source import Evidence
from daat.verification import verify_preparation


class FakeHostAuthentication:
    def verify(self, call):
        return VerifiedPrincipal(system="host-service", tenant="tenant-a",
                                 capabilities=frozenset({"daat-source-read"}),
                                 trusted=True, actor="actor-a")


class FakeGrant:
    def verify_grant(self, call, principal):
        return True


class FakeOutputVerifier:
    def verify(self, call, result, principal):
        return True


class FakeAudit:
    def __init__(self):
        self.events = []

    def record(self, record):
        self.events.append(record)


class FakeAllowPolicy:
    def evaluate(self, request):
        return BoundDecision(binding=request.binding, decision="ALLOW",
                             decision_id="test-decision-1", policy="test-policy-1",
                             valid_until=datetime.now(timezone.utc) + timedelta(seconds=35))


class FakeRejectPolicy:
    def evaluate(self, request):
        return BoundDecision(binding=request.binding, decision="DENY",
                             decision_id="test-decision-1", policy="test-policy-1",
                             valid_until=datetime.now(timezone.utc) + timedelta(seconds=35))


class FakeReader:
    def extract(self, call, principal):
        return OwnerExtraction(records=(Evidence("provider_record", "urn:owner:rec-1", "a"*64,
                                                 {"title":"Source claim"}, "external_unvalidated"),),
                               owner_source_sha256="a"*64, producer_revision="v1", rights_ref="urn:owner:rights1")


def call():
    return HostedSourceCall(admission_ref="test-admission-1", claimed_tenant="tenant-a",
                            claimed_system="host-service", adapter_id="host.metadata",
                            source_ref="urn:provider:metadata1", source_family_id="01",
                            source_revision="v1", purpose="metadata-research", requested_count=2, lane="L3")


def configured(*, policy=None, grants=None, verifier=None):
    return HostedOnramp(authenticator=FakeHostAuthentication(), source_grants=grants or FakeGrant(),
                        output_verifier=verifier or FakeOutputVerifier(), policy=policy or FakeAllowPolicy(),
                        audit=FakeAudit(), workers={"host.metadata": FakeReader()},
                        allowlist={"host.metadata": ("L3", "01")})


def test_host_requires_actual_injected_providers():
    with pytest.raises(AdmissionError):
        HostedOnramp().preview(call())


def test_hosted_source_path_enforces_actual_policy_and_output_verifier():
    host = configured()
    batch = host.preview(call())
    assert len(batch["records"]) == 1
    assert batch["authority"] == "noncanonical_unreviewed"
    assert batch["source"]["rights"]["verification"] == "trusted_host_grant_verifier"
    assert verify_preparation(batch)["valid"]


def test_hosted_source_denies_policy_and_unregistered_adapter():
    with pytest.raises(AdmissionError):
        configured(policy=FakeRejectPolicy()).preview(call())
    host = configured()
    host.allowlist.clear()
    with pytest.raises(AdmissionError):
        host.preview(call())


def test_hosted_source_cannot_skip_source_grant():
    class Deny:
        def verify_grant(self, call, principal):
            return False
    with pytest.raises(AdmissionError):
        configured(grants=Deny()).preview(call())


def test_hosted_source_rejects_raw_url_or_moving_ref():
    with pytest.raises(AdmissionError):
        HostedSourceCall(admission_ref="r", claimed_tenant="tenant-a", claimed_system="host-service",
                         adapter_id="host.metadata", source_ref="https://example.org/file", source_family_id="01",
                         source_revision="v1", purpose="research", requested_count=1, lane="L3")
