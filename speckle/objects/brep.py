from enum import Enum
from typing import List, Optional
from speckle.objects.base import SpeckleObjectBase


class TypeEnum(str, Enum):
    brep = 'brep'


class SpeckleObject(SpeckleObjectBase):
    type: TypeEnum = TypeEnum.brep
    # You can write a schema for the properties to make sure certain keys get in there
    properties: Optional[dict]
    displayMesh: str
