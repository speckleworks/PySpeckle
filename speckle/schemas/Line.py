import json
import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.schemas import Interval

NAME = 'line'

class Schema(SpeckleObject):
    type: Optional[str] = "Line"
    name: Optional[str] = "SpeckleLine"
    Value: List[float] = []
    domain: Optional[Interval] = Interval()

    class Config:
    	case_sensitive = False
