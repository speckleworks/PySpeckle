import json
import hashlib
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBaseSchema


NAME = 'interval'

class Schema(ResourceBaseSchema):
    type: str = "Interval"
    name: Optional[str] = "SpeckleInterval"
    Start: float = 0.0
    End: float = 0.0
    '''

    def dict(self):
        json_string = json.dumps(super(Schema, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(Schema, self).dict()

    '''
