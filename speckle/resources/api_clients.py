import uuid
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, UUID4, validator
from typing import List, Optional, Union
from speckle.base.resource import ResourceBase, ResourceBaseSchema
from speckle.resources.accounts import User
from enum import Enum

NAME = 'clients'
METHODS = ['list', 'create', 'get', 'update',
           'delete']


# class RoleEnum(str, Enum):
#     receiver: 'Receiver'
#     sender: 'Sender'
#     hybrid: 'Hybrid'


class ApiClient(ResourceBaseSchema):
    # role: Optional[RoleEnum] = RoleEnum.receiver
    role: Optional[str]
    documentName: Optional[str]
    documentType: Optional[str]
    documentLocation: Optional[str]
    documentGuid: Optional[str]
    streamId: Optional[str]
    online: Optional[bool]
    owner: Optional[Union[User, str]]

    @validator('documentGuid', pre=True, always=True)
    def set_guid(cls, v):
        return v or str(uuid.uuid4())

class Resource(ResourceBase):
    """API Access class for API Clients

    The `api_client` resource mostly returns an API Client data class instance.

    Example:
        Here is an example of what an API Client object looks like in dict form and when converted to a data class: 
        
        .. code-block:: python

            >>> from speckle.resources.api_clients import ApiClient
            >>> api_client_dict =  {
                    'role': 'Hybrid',
                    'documentName': 'Test',
                    'documentType': 'DataServer',
                    'documentLocation': 'http://some.server.com',
                    'online': True,
                }
            >>>  api_client = ApiClient.parse_obj(api_client_dict)
            >>> api_client.role
            'Hybrid'
            >>> api_client.documentGuid # Automatically created when document is instantiated if not specified
            'e991c923-cbb7-45f4-9488-e0f61ba006c0'



    """
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.schema = ApiClient

    def list(self):
        """List all API clients
        
        Returns:
            list -- A list of API client data class instances

    Example:
        Calling the `api_clients.list()` method returns a list of ApiClient class objects that the user has read access to.
        .. code-block:: python

            >>> client.api_clients.list()
            [<ApiClient>, <ApiClient>, <ApiClient>]
        """
        return self.make_request('list', '/')

    def create(self, data):
        """Create an API clients from a data dictionary
        
        Arguments:
            data {dict} -- A dictionary describing an API client
        
        Returns:
            ApiClient -- The instance created on the Speckle Server

    Example:        
        .. code-block:: python

            >>> api_client_dict =  {
                    'role': 'Hybrid',
                    'documentName': 'Test',
                    'documentType': 'DataServer',
                    'documentLocation': 'http://some.server.com',
                    'online': True,
                }
            >>> new_api_client = client.api_clients.create(data=api_client_dict)
            >>> new_api_client.id
            '54759eb3c090d83494e2d804'
            >>> new_api_client.documentName
            'Test'
        """
        return self.make_request('create', '/', data)

    def get(self, id):
        """Get a specific API client from the SpeckleServer
        
        Arguments:
            id {str} -- The ID of the API client to retrieve
        
        Returns:
            ApiClient -- The API client

    Example:        
        .. code-block:: python

            >>> api_client = client.api_clients.get('54759eb3c090d83494e2d804')
            >>> api_client.id
            '54759eb3c090d83494e2d804'
            >>> api_client.role
            'Hybrid'
            >>> api_client.dict()
            {
                'id'='54759eb3c090d83494e2d804',
                'private': False,
                'canRead': [],
                'canWrite': [],
                'owner': '7354308922443094682',
                'createdAt': '2019-06-09T20:23:22+00:00',
                'updatedAt': '2019-06-09T22:38:35+00:00',
                'role': 'Hybrid',
                'documentName': 'Test',
                'documentType': 'DataServer',
                'documentLocation': 'http://some.server.com',
                'online': True,
            }
        """
        return self.make_request('get', '/' + id)

    def update(self, id, data):
        """Update a specific API client
        
        Arguments:
            id {str} -- The ID of the API client to update
            data {dict} -- A dict of values to update
        
        Returns:
            dict -- a confirmation payload with the updated keys

    Example:        
        .. code-block:: python

            >>> api_client.id
            '54759eb3c090d83494e2d804'
            >>> client.api_clients.update(id=api_client.id, data={'documentName': 'newTest', 'documentLocation': 'https://some.new.server.com/dump'})
            {
                "success": True,
                "message": "Client updated following fields: ['documentName', 'documentLocation']"
            }
        """
        return self.make_request('update', '/' + id, data)

    def delete(self, id):
        """Delete a specific API client
        
        Arguments:
            id {str} -- The ID of the API client to delete
        
        Returns:
            dict -- A confirmation payload

    Example:
        .. code-block:: python

            >>> api_client.id
            '54759eb3c090d83494e2d804'
            >>> client.api_clients.delete(id=api_client.id)
            {
                "success": True,
                "message": 'Client was deleted! Bye bye data.'"
            }
        """
        return self.make_request('delete', '/' + id)
