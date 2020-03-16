import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.schemas import Mesh

NAME = 'brep'

class Schema(ResourceBaseSchema):
    type: Optional[str] = "Brep"
    name: Optional[str] = "SpeckleBrep"
    geometryHash: Optional[str]  # Is immediately replaced anyways
    hash: Optional[str]  # Is immediately replaced anyways
    applicationId: Optional[str]
    properties: Optional[dict]
    partOf: Optional[List[str]]
    parent: Optional[List[str]]
    children: Optional[List[str]]
    ancestors: Optional[List[str]]
    displayValue: Optional[Mesh.Schema]
    rawData: str = ""

    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()
