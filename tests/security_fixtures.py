"""Synthetic ONLY. Not for real authentication or production authorization."""
from datetime import datetime,timezone,timedelta
from daat.security import BoundDecision

class SyntheticPolicy:
    def __init__(self,decision='ALLOW', obligations=(), expire_seconds=30, tamper=False):
        self.decision=decision;self.obligations=tuple(obligations)
        self.expire_seconds=expire_seconds;self.tamper=tamper
        self.requests=[]
    def evaluate(self,req):
        self.requests.append(req)
        return BoundDecision(binding='0'*64 if self.tamper else req.binding,
            decision=self.decision,decision_id='PD-synthetic',policy='fake-policy/1',
            valid_until=datetime.now(timezone.utc)+timedelta(seconds=self.expire_seconds),
            obligations=self.obligations)

class SyntheticAudit:
    def __init__(self,broken=False):self.items=[];self.broken=broken
    def record(self,record):
        if self.broken:raise OSError('fake audit unavailable')
        self.items.append(record)
