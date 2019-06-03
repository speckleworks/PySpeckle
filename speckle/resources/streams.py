import uuid
from pydantic import BaseModel, UUID4, validator, Schema
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema
from speckle.resources.objects import SpeckleObject
from speckle.resources.api_clients import ApiClient

NAME = 'streams'
METHODS = ['list', 'create', 'get', 'update',
           'delete', 'comment_get', 'comment_create',
           'clone', 'diff', 'list_objects', 'list_clients']


class LayerProperties(BaseModel):
  color: dict = {}
  visible: bool = True
  pointsize: float = 0
  linewidth: float = 0
  shininess: float = 0
  smooth: bool = True
  showEdges: bool = True
  wireframe: bool = True


class Layer(BaseModel):
    guid: str
    name: str = 'New Layer'
    orderIndex: int = 0
    startIndex: int = 0
    objectCount: int = 0
    topology: Optional[str]
    properties: Optional[LayerProperties]

    @validator('guid', pre=True, always=True)
    def set_guid(cls, v):
        return v or str(uuid.uuid4())


class Stream(ResourceBaseSchema):
    streamId: Optional[str]
    name: Optional[str]
    description: Optional[str]
    tags: List[str] = []
    commitMessage: str  = 'Modified stream'
    objects: List[SpeckleObject] = []
    layers: List[Layer] = []
    parent: Optional[str]
    children: List[str] = []

class Resource(ResourceBase):
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.method_dict.update({
            'clone': {
                'method': 'POST'
            },
            'diff': {
                'method': 'GET'
            },
            'list_objects': {
                'method': 'GET'
            },
            'list_clients': {
                'method': 'GET'
            }
        })

        self.schema = Stream


    def clone(self, id, name=None):
        response = self.make_request('clone', '/' + id + '/clone', {'name': name})
        clone = self._parse_response(response['clone'])
        parent = self._parse_response(response['parent'])
        return clone, parent

    def diff(self, id, other_id):
        return self.make_request('diff', '/' + id + '/diff/' + other_id)

    def list_objects(self, id):
        return self.make_request('list_objects', '/' + id + '/objects', schema=SpeckleObject)

    def list_clients(self, id):
        return self.make_request('list_clients', '/' + id + '/clients', schema=ApiClient)

    def list(self):
        return self.make_request('list', '?omit=objects')  
