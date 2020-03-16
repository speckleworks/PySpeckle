import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.schemas import Interval

NAME = 'polycurve'

class Schema(SpeckleObject):
    type: Optional[str] = "Polycurve"
    name: Optional[str] = "SpecklePolycurve"
    Segments: List[dict] = []
    Domain: 'Interval' = Interval()
    Closed: bool = False
