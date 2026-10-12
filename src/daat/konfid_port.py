"""Adapter for *existing* Konfid AccessRequest/AccessResponse, via trusted host RPC.

The supplied call function MUST implement authenticated, confidential transport,
workload and actor binding, TLS verification, bounded timeouts and response size,
plus producer response provenance. This module does NOT provide those controls.
"""
from __future__ import annotations
from datetime import datetime
from typing import Callable, Mapping, Any
from .security import PolicyRequest,BoundDecision
from .errors import AdmissionError

class KonfidPolicyPort:
    def __init__(self,trusted_evaluate_access:Callable[[dict],Mapping[str,Any]]):
        if not callable(trusted_evaluate_access): raise ValueError('trusted evaluator is mandatory')
        self._call=trusted_evaluate_access

    def evaluate(self,request:PolicyRequest)->BoundDecision:
        raw=self._call(request.konfid_request())
        if not isinstance(raw,Mapping): raise AdmissionError('POLICY_INVALID','Malformed Konfid response')
        expiry=raw.get('valid_until')
        if isinstance(expiry,str):
            try: expiry=datetime.fromisoformat(expiry.replace('Z','+00:00'))
            except ValueError as exc: raise AdmissionError('POLICY_INVALID','Invalid expiry') from exc
        obs=raw.get('obligations',[])
        if not isinstance(obs,list): raise AdmissionError('POLICY_INVALID','Malformed obligations')
        # Bind only on the trusted adapter side, never to a client-supplied field.
        return BoundDecision(
            binding=request.binding,decision=raw.get('decision'),
            decision_id=raw.get('decision_id'),policy=raw.get('policy'),
            valid_until=expiry,obligations=tuple(obs))
