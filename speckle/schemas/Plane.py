import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.schemas import Point, Vector

NAME = 'plane'

class Schema(SpeckleObject):
    type: Optional[str] = "Plane"
    name: Optional[str] = "SpecklePlane"
    origin: Point.Schema = Point.Schema(Value=[0,0,0])
    normal: Vector.Schema = Vector.Schema(Value=[0,0,1])
    xdir: Vector.Schema = Vector.Schema(Value=[1,0,0])
    ydir: Vector.Schema = Vector.Schema(Value=[0,1,0])
