import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.schemas import Interval

NAME = 'polycurve'

class Schema(SpeckleObject):
    type: Optional[str] = "Polycurve"
    name: Optional[str] = "SpecklePolycurve"
    Segments: List[dict] = []
    Domain: 'Interval' = Interval()
    Closed: bool = False

    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()
