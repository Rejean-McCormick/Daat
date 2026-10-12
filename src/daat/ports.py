"""Only contracts/ports. Host IK and Kristal implementations remain external."""
from typing import Any, Mapping, Protocol

class MappingProfilePort(Protocol):
    id:str
    version:str
    def map_export(self,manifest:Mapping[str,Any])->Mapping[str,Any]: ...

class KristalNativePort(Protocol):
    def compile(self,structured_input:Mapping[str,Any],*,requested_outputs:list[str])->list[Mapping[str,Any]]: ...
