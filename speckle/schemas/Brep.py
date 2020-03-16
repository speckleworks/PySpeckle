import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.schemas import Mesh
from speckle.resources.objects import SpeckleObject

NAME = 'brep'

class Schema(SpeckleObject):
    type: Optional[str] = "Brep"
    name: Optional[str] = "SpeckleBrep"
    displayValue: Optional[Mesh.Schema]
    rawData: str = ""
