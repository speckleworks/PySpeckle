from enum import Enum
from typing import List, Optional
from speckle.objects.base import SpeckleObjectBase

class TypeEnum(str, Enum):
    mesh = 'mesh'


class SpeckleObject(SpeckleObjectBase):
    type: TypeEnum = TypeEnum.mesh
    # You can write a schema for the properties to make sure certain keys get in there
    properties: Optional[dict]
    vertices: List[float]
    faces: List[int]
