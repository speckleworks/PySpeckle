import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject

NAME = 'mesh'

class Schema(SpeckleObject):
    type: str = "Mesh"
    name: Optional[str] = "SpeckleMesh"
    vertices: List[float] = []
    faces: List[int] = []
    texture_coordinates: Optional[List[float]]
    colors: Optional[List[int]]
