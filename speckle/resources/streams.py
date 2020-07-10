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

class StreamBaseProperties(BaseModel):
    units: str = "Meters" # Set default units if none are found
    tolerance: Optional[float]# = 1.0e-2
    angleTolerance: Optional[float]# = 1.0e-2

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
    baseProperties: Optional[StreamBaseProperties] = StreamBaseProperties()

class Resource(ResourceBase):
    """API Access class for Streams

    """
    
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

    def list(self, query={'omit':'objects'}):
        """List all streams
        
        Returns:
            list -- A list of Streams, without objects attached
        """
        return self.make_request('list', '/', params=query)

    def create(self, data):
        """Create a stream from a data dictionary
        
        Arguments:
            data {dict} -- A dictionary describing a stream
        
        Returns:
            Stream -- The instance created on the Speckle Server
        """
        return self.make_request('create', '/', data)

    def get(self, id, query=None):
        """Get a specific stream from the SpeckleServer
        
        Arguments:
            id {str} -- The StreamId of the stream to retrieve
        
        Returns:
            Stream -- The stream
        """
        return self.make_request('get', '/' + id, params=query)

    def update(self, id, data):
        """Update a specific stream
        
        Arguments:
            id {str} -- The StreamId of the stream to update
            data {dict} -- A dict of values to update
        
        Returns:
            dict -- a confirmation payload with the updated keys
        """
        return self.make_request('update', '/' + id, data)

    def delete(self, id):
        """Delete a specific stream
        
        Arguments:
            id {str} -- The StreamId of the stream to delete
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('delete', '/' + id)

    def comment_get(self, id):
        """Retrieve comments attached to a stream
        
        Arguments:
            id {str} -- The StreamId of the stream to retrieve comments from
        
        Returns:
            list -- A list of comments
        """
        return self.make_request('comment_get', '/' + id, comment=True)

    def comment_create(self, id, data):
        """Add a comment to a stream
        
        Arguments:
            id {str} -- The StreamId of the stream to comment on
            data {dict} -- A comment dictionary object
        
        Returns:
            CommentSchema -- The comment created by the server
        """
        return self.make_request('comment_create', '/' + id, data, comment=True)


    def clone(self, id, name=None):
        """Clone a stream
        
        Arguments:
            id {str} -- The StreamId of the stream to clone
        
        Keyword Arguments:
            name {str} -- The name of the new cloned stream. eg: stream-x-2019-06-09-backup (default: {None})
        
        Returns:
            tuple -- The clone and parent stream as dicts
        """
        response = self.make_request('clone', '/' + id + '/clone', {'name': name})
        clone = self._parse_response(response['clone'])
        parent = self._parse_response(response['parent'])
        return clone, parent

    def diff(self, id, other_id):
        """Runs a diff on two streams
        
        Arguments:
            id {str} -- StreamId of the main stream
            other_id {str} -- StreamId of the stream to compare
        
        Returns:
            dict -- A response payload with objects and layers as keys
        """
        return self.make_request('diff', '/' + id + '/diff/' + other_id)

    def list_objects(self, id, query=None):
        """Return the list of objects in a stream
        
        Arguments:
            id {str} -- StreamId of the stream to list objects from
        
        Returns:
            list -- A list of Speckle objects
        """
        return self.make_request('list_objects', '/' + id + '/objects', schema=SpeckleObject, params=query)

    def list_clients(self, id):
        """Return the list of api clients connected to the stream
        
        Arguments:
            id {str} -- StreamId of the stream to list objects from
        
        Returns:
            list -- A list of API clients
        """
        return self.make_request('list_clients', '/' + id + '/clients', schema=ApiClient)
