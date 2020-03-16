import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.schemas import Mesh
from speckle.resources.objects import SpeckleObject

NAME = 'brep'

class Schema(SpeckleObject):
    type: Optional[str] = "Brep"
    name: Optional[str] = "SpeckleBrep"
    displayValue: Optional[Mesh.Schema]
    rawData: str = ""

    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()
