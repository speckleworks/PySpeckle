import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject


NAME = 'point'

class Schema(SpeckleObject):
    type: str = "Point"
    name: Optional[str] = "SpecklePoint"
    value: List[float] = [0,0,0]
