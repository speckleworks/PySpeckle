from pydantic import BaseModel
from typing import Optional
from speckle.base.resource import ResourceBase


NAME = 'accounts'
METHODS = ['get', 'get_profile', 'update_profile', 'set_role', 'search']


class User(BaseModel):
    id: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    company: Optional[str]
    avatar: Optional[str]
    role: Optional[str]

    class Config:
        fields = {'id': '_id'}

class Resource(ResourceBase):
    """API Access class for Accounts
    
    The accounts resource is used to search, retrieve and manipulate user profiles. None of the methods return an instanciated data class, instead they all return dictionary payloads.

    Example:
        Here is an example of what an account object looks like: 
        
        .. code-block:: python

            {
                "id": "507f1f77bcf86cd799439011"
                "name": "Test"
                "surname": "McTestyFace"
                "company": "Acme"
                "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                "role": "user"
            }
    
    """
    
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        # self.schema = User

        self.method_dict.update({
            'get_profile': {
                'method': 'GET'
            },
            'update_profile': {
                'method': 'PUT'
            },
            'set_role': {
                'method': 'PUT'
            },
            'search': {
                'method': 'POST'
            },
        })


    def get(self, id):
        """Get a specific user from the SpeckleServer

        Arguments:
            id {str} -- The ID of the resource to retrieve
        
        Returns:
            dict -- The user

        Example:
            .. code-block:: python

                >>> user_id = '507f1f77bcf86cd799439011'
                >>> client.accounts.get(id=user_id)
                {
                    "success": True,
                    "resource": {
                        "id": "507f1f77bcf86cd799439011",
                        "email": "test@test.com"
                        "name": "Test"
                        "surname": "McTestyFace"
                        "company": "Acme"
                        "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                        "role": "user"
                    }
                }
        """
        return self.make_request('get', '/' + id)

    def get_profile(self):
        """Get current logged in user's profile
        
        Returns:
            dict -- The current user's profile

        Example:
            .. code-block:: python

                >>> from speckle.SpeckleClient import SpeckleApiClient
                >>> client = SpeckleApiClient(host='hestia.speckle.com')
                >>> client.login(email='test@test.com', password='somesupersecret')
                >>> client.accounts.get_profile()
                {
                    "success": True,
                    "resource": {
                        "id": "507f1f77bcf86cd799439011",
                        "email": "test@test.com"
                        "name": "Test"
                        "surname": "McTestyFace"
                        "company": "Acme"
                        "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                        "role": "user"
                    }
                }
        """
        return self.make_request('get_profile', '/')

    def update_profile(self, data):
        """Update the current logged in user's profile
        
        Arguments:
            data {dict} -- A dictionary of profile values to be updated
        
        Returns:
            dict -- A confirmfation payload of the updated keys

        Example:
            .. code-block:: python

                >>> from speckle.SpeckleClient import SpeckleApiClient
                >>> client = SpeckleApiClient(host='hestia.speckle.com')
                >>> client.login(email='test@test.com', password='somesupersecret')
                >>> client.accounts.get_profile()
                {
                    "success": True,
                    "resource": {
                        "id": "507f1f77bcf86cd799439011",
                        "email": "test@test.com"
                        "name": "Test"
                        "surname": "McTestyFace"
                        "company": "Acme"
                        "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                        "role": "user"
                    }
                }
                >>> client.accounts.update_profile({'name': 'Tester'})
                { 
                    "success": True,
                    "message": 'User profile updated.'
                }

        """
        return self.make_request('update_profile', '/', data)

    def set_role(self, id, role):
        """Set the role of a user

        Warning:
            The client must be authenticated with an `admin` user to carry
            out this operation.
        
        Arguments:
            id {str} -- The ID of the user to be updated
            role {str} -- The role to give the user ('admin' or 'user')
        
        Returns:
            dict -- A response payload confirming the user role update

        Example:
            .. code-block:: python

                >>> from speckle.SpeckleClient import SpeckleApiClient
                >>> client = SpeckleApiClient(host='hestia.speckle.com')
                >>> client.login(email='test@test.com', password='somesupersecret')
                >>> client.accounts.get_profile()
                {
                    "success": True,
                    "resource": {
                        "id": "507f1f77bcf86cd799439011",
                        "email": "test@test.com"
                        "name": "Test"
                        "surname": "McTestyFace"
                        "company": "Acme"
                        "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                        "role": "admin"
                    }
                }
                >>> user_to_modify = '9eeb71aa8b2a292512a3bf94091e2df8'
                >>> client.accounts.set_role(id=user_to_modify, role='admin')
                { 
                    "success": True,
                    "message": 'User profile updated.'
                }
        """
        data = {'role': role}
        return self.make_request('set_role', '/' + id, data)

    def search(self, search):
        """Search for one or more users
        
        Arguments:
            search {str} -- A search string. Should be at least 3 characters long.

        Returns:
            list -- A list of found users

        Example:
            .. code-block:: python

                >>> client.accounts.search('tom')
                {
                    "success": True,
                    "resources": [{
                        "id": "507f1f77bcf86cd799439011",
                        "email": "tom@test.com"
                        "name": "Tom"
                        "surname": "Svilans"
                        "company": "Acme"
                        "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                        "role": "admin"
                    },
                    {
                        "id": "397f19073b30eb9f71fc5bas",
                        "email": "test@tom.com"
                        "name": "Test"
                        "surname": "McTestyFace"
                        "company": "Tom Associated"
                        "avatar": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDzvciiQ5-P6itEjycriGb9l9sJH9E538C-tM9QRgFVTaj0Muq"
                        "role": "user"
                    },
                    {
                        "id": "9bfb9894c21e29014cd0e8166",
                        "email": "tom@tom.com"
                        "name": "Tom"
                        "surname": "Tom"
                        "company": "Tom"
                        "avatar": "https://i.ytimg.com/vi/Dtm5nMlqq1Q/maxresdefault.jpg"
                        "role": "admin"
                    }]

                }
        """
        data = {
            'searchString': search
        }

        return self.make_request('search', 'search', data)
