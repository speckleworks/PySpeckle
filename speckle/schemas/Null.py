import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject


NAME = 'null'

class Schema(SpeckleObject):
    type: Optional[str] = "Null"
    name: Optional[str] = "SpeckleNull"