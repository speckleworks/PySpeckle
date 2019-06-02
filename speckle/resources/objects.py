import json
import hashlib
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema

NAME = 'objects'
METHODS = ['list', 'get', 'update',
           'delete', 'comment_get', 'comment_create']


class SpeckleObject(ResourceBaseSchema):
    type: Optional[str]
    name: Optional[str]
    geometryHash: Optional[str]  # Is immediately replaced anyways
    hash: Optional[str]  # Is immediately replaced anyways
    applicationId: Optional[str]
    properties: dict = {}
    partOf: Optional[List[str]]
    parent: Optional[List[str]]
    children: Optional[List[str]]
    ancestors: Optional[List[str]]


    def dict(self):
        json_string = json.dumps(super(SpeckleObject, self).dict()['properties'])

        self.geometryHash = hashlib.md5(
            json_string.encode('utf-8')).hexdigest()

        self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(SpeckleObject, self).dict()


class Resource(ResourceBase):
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.method_dict.update({
            'get_bulk': {
                'method': 'POST'
            },
            'set_properties': {
                'method': 'PUT'
            }
        })
           
        self.schema = SpeckleObject

    def get_bulk(self, data):
        return self.make_request('get_bulk', '/getbulk', data)

    def set_properties(self, id, data):
        return self.make_request('set_properties', '/' + id + '/properties', data)
