import json
import hashlib
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema

NAME = 'objects'
METHODS = ['list', 'get', 'update', 'create',
           'delete', 'comment_get', 'comment_create',
           'get_bulk', 'set_properties']


class SpeckleObject(ResourceBaseSchema):
    type: Optional[str]
    name: Optional[str] # Name is often null
    geometryHash: Optional[str]  # Is immediately replaced anyways
    hash: Optional[str]  # Is immediately replaced anyways
    applicationId: Optional[str]
    properties: Optional[dict] # Some objects have null properties
    partOf: Optional[List[str]]
    parent: Optional[List[str]]
    children: Optional[List[str]]
    ancestors: Optional[List[str]]

    
    def dict(self, include=None, exclude=None, by_alias=True, exclude_unset=False, exclude_defaults=False, exclude_none=False):
        json_string = json.dumps(super(SpeckleObject, self).dict()['properties'])

        self.geometryHash = hashlib.md5(json_string.encode('utf-8')).hexdigest()

        #self.hash = hashlib.md5('{}.{}'.format(self.type, json_string).encode('utf-8')).hexdigest()

        return super(SpeckleObject, self).dict(include=include, by_alias=True, exclude=exclude)
    
    class Config():
        extra = 'allow'

class Resource(ResourceBase):
    """API Access class for Speckle Objects

    """
    
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

    def list(self, query=None):
        """List all Speckle objects
        
        Returns:
            list -- A list of Speckle object data class instances
        """
        query_string = self.make_query(query)        
        return self.make_request('list', '/' + query_string)

    def create(self, data):
        """Create a Speckle object from a data dictionary
        
        Arguments:
            data {dict} -- A dictionary describing a Speckle object
        
        Returns:
            SpeckleObject -- The instance created on the Speckle Server
        """
        return self.make_request('create', '/', data)

    def get(self, id, query=None):
        """Get a specific Speckle object from the SpeckleServer
        
        Arguments:
            id {str} -- The ID of the Speckle object to retrieve
        
        Returns:
            SpeckleObject -- The Speckle object
        """
        return self.make_request('get', '/' + id, params=query)


    def update(self, id, data):
        """Update a specific Speckle object
        
        Arguments:
            id {str} -- The ID of the Speckle object to update
            data {dict} -- A dict of values to update
        
        Returns:
            dict -- a confirmation payload with the updated keys
        """
        return self.make_request('update', '/' + id, data)

    def delete(self, id):
        """Delete a specific Speckle object
        
        Arguments:
            id {str} -- The ID of the Speckle object to delete
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('delete', '/' + id)

    def comment_get(self, id):
        """Retrieve comments attached to a Speckle object
        
        Arguments:
            id {str} -- The ID of the Speckle object to retrieve comments from
        
        Returns:
            list -- A list of comments
        """
        return self.make_request('comment_get', '/' + id, comment=True)

    def comment_create(self, id, data):
        """Add a comment to a Speckle object
        
        Arguments:
            id {str} -- The ID of the Speckle object to comment on
            data {dict} -- A comment dictionary object
        
        Returns:
            CommentSchema -- The comment created by the server
        """
        return self.make_request('comment_create', '/' + id, data, comment=True)

    def get_bulk(self, object_ids, query=None):
        """Retrieve and optionally update a list of Speckle objects
        
        Arguments:
            object_ids {list} -- A list of object IDs
            query {dict} -- A dictionary to specifiy which fields to retrieve, filters, limits, etc
        
        Returns:
            list -- A list of SpeckleObjects
        """
        return self.make_request('get_bulk', '/getbulk', object_ids, params=query)

    def set_properties(self, id, data):
        return self.make_request('set_properties', '/' + id + '/properties', data)
