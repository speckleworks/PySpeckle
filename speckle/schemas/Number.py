import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject


NAME = 'number'

class Schema(SpeckleObject):
    type: str = "Number"
    name: Optional[str] = "SpeckleNumber"
    value: float = 0.0
