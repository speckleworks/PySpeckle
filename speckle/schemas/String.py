import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject


NAME = 'string'

class Schema(SpeckleObject):
    type: str = "String"
    name: Optional[str] = "SpeckleString"
    value: str = ""
