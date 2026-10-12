"""SYNTHETIC IN-PROCESS DEMO. Never use these accept-all verifiers for real systems."""
from pathlib import Path
import json
from daat.bridge import V6BuildBridge,VerifiedPrincipal
from daat.security import BoundDecision
from datetime import datetime,timezone,timedelta

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def load(name):return json.loads((HERE/name).read_text(encoding='utf-8'))

class DemoOnlyAuthentication:
    def verify(self,envelope):
        # Test fixture identity, NOT cryptographic verification.
        if envelope['source']['system']!='orgo': raise PermissionError('test fixture only')
        return VerifiedPrincipal('orgo','school-demo',frozenset({'kristal-build'}),True,actor='svc:orgo')

class DemoOnlyArtifactVerifier:
    def verify(self,ref,principal):
        # Tests trusted fixtures only; NEVER a production bytes/hash verifier.
        return ref['artifact_id'] in ('sample-1','synthetic-kristal-state-1')

class DemoOnlyManifestVerifier:
    def verify(self,manifest,principal):
        # No cryptographic integrity check: simulator input only.
        return manifest['id']=='export-test-123'

class DemoOnlyKristal:
    def compile(self,structured_input,*,requested_outputs):
        assert structured_input['id']=='export-test-123'
        assert requested_outputs==['kristal_state']
        return [{
            'owner':{'system':'kristal','organization':'school-demo'},
            'artifact_type':'kristal_state','artifact_id':'synthetic-kristal-state-1',
            'locator':{'ref':'urn:kristal:synthetic:1'},
            'integrity':{'algorithm':'sha256','digest':'sha256:'+'a'*64}
        }]

class DemoOnlyKonfidPolicy:
    # TEST FIXTURE: not a Konfid/kOA policy decision or authenticated transport.
    def evaluate(self,request):
        return BoundDecision(request.binding,'ALLOW','PD-SYNTHETIC','demo-only/v1',
                             datetime.now(timezone.utc)+timedelta(seconds=30))

class DemoOnlyAudit:
    # TEST FIXTURE: in-memory list, NOT a persistent authoritative audit broker.
    def __init__(self):self.records=[]
    def record(self,item):self.records.append(item)

def main():
    bridge=V6BuildBridge(DemoOnlyAuthentication(),DemoOnlyArtifactVerifier(),DemoOnlyManifestVerifier(),
                         policy=DemoOnlyKonfidPolicy(),audit=DemoOnlyAudit())
    e=load('ik-build-envelope.json');m=load('ik-export-manifest.json')
    out=bridge.process(e,m,ROOT/'mappings/native/profile.json',DemoOnlyKristal())
    print(json.dumps({'DEMO_ONLY':True,'acceptance':out.acceptance,'final':out.final,
                      'event':out.event},indent=2))

if __name__=='__main__':main()
