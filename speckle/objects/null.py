from enum import Enum
from typing import List, Optional
from speckle.objects.base import SpeckleObjectBase


class TypeEnum(str, Enum):
    null = 'null'


class SpeckleObject(SpeckleObjectBase):
    type: TypeEnum = TypeEnum.null
