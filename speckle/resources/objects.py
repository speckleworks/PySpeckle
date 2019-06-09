import json
import hashlib
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, validator
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema

NAME = 'objects'
METHODS = ['list', 'get', 'update', 'create'
           'delete', 'comment_get', 'comment_create',
           'get_bulk', 'set_properties']


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

    def list(self):
        """List all Speckle objects
        
        Returns:
            list -- A list of Speckle object data class instances
        """
        return self.make_request('list', '/')

    def create(self, data):
        """Create a Speckle object from a data dictionary
        
        Arguments:
            data {dict} -- A dictionary describing a Speckle object
        
        Returns:
            SpeckleObject -- The instance created on the Speckle Server
        """
        return self.make_request('create', '/', data)

    def get(self, id):
        """Get a specific Speckle object from the SpeckleServer
        
        Arguments:
            id {str} -- The ID of the Speckle object to retrieve
        
        Returns:
            SpeckleObject -- The Speckle object
        """
        return self.make_request('get', '/' + id)

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

    def get_bulk(self, object_ids, query):
        """Retrieve and optionally update a list of Speckle objects
        
        Arguments:
            object_ids {list} -- A list of object IDs
            query {dict} -- A dictionary to specifiy which fields to retrieve, filters, limits, etc
        
        Returns:
            list -- A list of SpeckleObjects
        """
        query_string = '?'

        for key, value in query.items:
            query_string += key + '='
            if isinstance(value, list):
                query_string += ','.join(value)
            elif isinstance(value, str):
                query_string += value + '&'
            else:
                raise 'query dict values must be list or string but key {} is of type {}'.format(key, type(value))

        query_string = query_string[:-1] # Remove last '&' or '?' to be clean

        return self.make_request('get_bulk', '/getbulk' + query_string, object_ids)

    def set_properties(self, id, data):
        return self.make_request('set_properties', '/' + id + '/properties', data)
