import uuid
from pydantic import BaseModel, UUID4, validator, Schema
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema
from speckle.resources.objects import SpeckleObject

NAME = 'streams'
METHODS = ['list', 'create', 'get', 'update',
           'delete', 'comment_get', 'comment_create']


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
    guid: UUID4
    name: str = 'New Layer'
    orderIndex: int = 0
    startIndex: int = 0
    objectCount: int = 0
    topology: Optional[str]
    properties: Optional[LayerProperties]

    @validator('guid', pre=True, always=True)
    def set_guid(cls, v):
        return v or uuid.uuid4()


class Stream(ResourceBaseSchema):
    name: Optional[str]
    description: Optional[str]
    tags: List[str] = []
    commitMessage: str  = 'Modified stream'
    objects: List[SpeckleObject] = []
    layers: List[Layer] = []


class Resource(ResourceBase):
    def __init__(self, session, basepath):
        super().__init__(session, basepath, NAME, METHODS)

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


    def clone(self, id):
        return self.make_request('clone', '/' + id + '/clone')

    def diff(self, id, other_id):
        return self.make_request('diff', '/' + id + '/diff/' + other_id)

    def list_objects(self, id):
        return self.make_request('list_objects', '/' + id + '/objects')

    def list_clients(self, id):
        return self.make_request('list_clients', '/' + id + '/clients')
