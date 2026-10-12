"""Compatibility with IK's published MappingProfile.map_export protocol."""
from __future__ import annotations
from pathlib import Path
from typing import Any,Mapping
from .mapping import load_profile,apply

class DeclarativeMappingAdapter:
    def __init__(self,path:Path):
        self.profile,self.source,self.target=load_profile(path)
        self.id=self.profile['id'];self.version=self.profile['version']
    def map_export(self,manifest:Mapping[str,Any])->Mapping[str,Any]:
        return apply(self.profile,self.source,self.target,dict(manifest))
