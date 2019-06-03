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

    def get_profile(self):
        return self.make_request('get_profile', '/')

    def update_profile(self, data):
        return self.make_request('update_profile', '/', data)

    def set_role(self, id, role):
        data = {'role': role}
        return self.make_request('set_role', '/' + id, data)

    def search(self, data):
        return self.make_request('search', 'search', data)
