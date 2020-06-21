import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject


NAME = 'vector'

class Schema(SpeckleObject):
    type: str = "Vector"
    name: Optional[str] = "SpeckleVector"
    value: List[float] = [0,0,1]
