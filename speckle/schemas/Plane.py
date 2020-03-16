import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.schemas import Point, Vector

NAME = 'plane'

class Schema(ResourceBaseSchema):
    type: Optional[str] = "Plane"
    Origin: Point.Schema = Point.Schema(Value=[0,0,0])
    Normal: Vector.Schema = Vector.Schema(Value=[0,0,1])
    Xdir: Vector.Schema = Vector.Schema(Value=[1,0,0])
    Ydir: Vector.Schema = Vector.Schema(Value=[0,1,0])

    '''
    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()
    '''
