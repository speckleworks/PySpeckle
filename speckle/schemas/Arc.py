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
    Radius: float = 0.0
    StartAngle: float = 0.0
    EndAngle: float = 0.0
    AngleRadians: float = 0.0
    Domain: Interval.Schema = Interval.Schema()
    Plane: Plane = Plane.Schema()

    '''
    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()
    '''
