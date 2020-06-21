import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject

NAME = 'polyline'

class Schema(SpeckleObject):
    type: str = "Polyline"
    name: Optional[str] = "SpecklePolyline"
    value: List[float] = []

    #class Config:
    #	fields={'Value':'value'}
