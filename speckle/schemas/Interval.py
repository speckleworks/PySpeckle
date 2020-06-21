import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema

NAME = 'interval'

class Schema(ResourceBaseSchema):
    type: str = "Interval"
    name: Optional[str] = "SpeckleInterval"
    start: float = 0.0
    end: float = 0.0
