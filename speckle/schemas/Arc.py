import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.schemas import Plane, Interval

NAME = 'arc'

class Schema(SpeckleObject):
    type: Optional[str] = "Arc"
    name: Optional[str] = "SpeckleArc"
    radius: float = 0.0
    startAngle: float = 0.0
    endAngle: float = 0.0
    angleRadians: float = 0.0
    domain: Interval.Schema = Interval.Schema()
    plane: Plane.Schema = Plane.Schema()
