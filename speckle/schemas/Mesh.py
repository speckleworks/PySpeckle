import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema

NAME = 'mesh'

class Schema(ResourceBaseSchema):
    type: Optional[str] = "Mesh"
    name: Optional[str] = "SpeckleMesh"
    geometryHash: Optional[str]  # Is immediately replaced anyways
    hash: Optional[str]  # Is immediately replaced anyways
    applicationId: Optional[str]
    properties: Optional[dict]
    partOf: Optional[List[str]]
    parent: Optional[List[str]]
    children: Optional[List[str]]
    ancestors: Optional[List[str]]
    vertices: List[float] = []
    faces: List[int] = []
    texture_coordinates: Optional[List[float]]
    colors: Optional[List[int]]


    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()
