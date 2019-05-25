from pydantic import BaseModel
from typing import Optional
from speckle.base.resource import ResourceBase


NAME = 'accounts'
METHODS = ['get', 'delete']


class UserSearch(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    company: Optional[str] = None

class User(UserSearch):
    avatar: Optional[str] = None

class Role(BaseModel):
    role: str

class Resource(ResourceBase):
    def __init__(self, session, basepath):
        super().__init__(session, basepath, NAME, METHODS)

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

    def get_profile(self):
        return self.make_request('get_profile', '/')

    def update_profile(self, data):
        return self.make_request('update_profile', '/', data)

    def set_role(self, id, data):
        return self.make_request('set_role', '/' + id, data)

    def search(self, data):
        return self.make_request('search', 'search', data)
