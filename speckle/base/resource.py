import json
from requests import Request
from pydantic import BaseModel
from typing import List, Optional
import dataclasses
from dataclasses import dataclass
from datetime import datetime

class ResourceBaseSchema(BaseModel):
    id: Optional[str] # Optional[str]
    private: Optional[bool]
    canRead: Optional[List[str]]
    canWrite: Optional[List[str]]
    anonymousComments: Optional[bool]
    comments: Optional[List[str]]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    class Config:
        fields = {'id': '_id'}


class Comment(ResourceBaseSchema):
    resource: dict = {}
    text: str
    assignedTo: Optional[List[str]]
    closed: Optional[bool]
    labels: Optional[List[str]]
    view: dict = {}
    screenshot: str = None


def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

class ResourceBase(object):

    def __init__(self, session, basepath, name, methods):
        self.s = session
        self._path = basepath + '/' + name
        self._comment_path = basepath + '/comments/' + name
        self.name = name
        self.methods = methods
        self.method_dict = {
            'list': {
                'method': 'GET',
                },
            'create': {
                'method': 'POST',
                },
            'get': {
                'method': 'GET',
                },
            'update': {
                'method': 'PUT',
                },
            'delete': {
                'method': 'DELETE',
                },
            'comment_get': {
                'method': 'GET',
                },
            
            'comment_create': {
                'method': 'POST'}
        }

        for method in self.methods:
            if method == 'retrieve':
                self.__setattr__('retrieve', 'x')

        self.schema = None
        self.comment_schema = Comment

    def _prep_request(self, method, path, comment, data):
        assert method in self.methods, 'method {} not supported for {} calls'.format(method, self.name)

        if comment:
            url = self._comment_path + path
            if data:
                dataclass_instance = self.comment_schema.parse_obj(data)
                data = clean_empty(dataclass_instance.dict()) 
        else:
            url = self._path + path
            if data:
                if self.schema:
                    dataclass_instance = self.schema.parse_obj(data)
                    data = clean_empty(dataclass_instance.dict())

        return self.s.prepare_request(Request(self.method_dict[method]['method'], url, json=data))

    def _parse_response(self, response, comment):
        print(json.dumps(response, indent=2))
        if comment:
            return self.comment_schema.parse_obj(response)
        else:
            return self.schema.parse_obj(response)


    def make_request(self, method, path, data=None, comment=False):
        r = self._prep_request(method, path, comment, data)
        resp = self.s.send(r)

        assert resp.status_code == 200, 'Something went wrong calling the server'

        response_payload = resp.json()
        assert response_payload['success'] == True, 'Something went wrong with the server... :('
        
        if 'resources' in response_payload:
            return [self._parse_response(resource, comment) for resource in response_payload['resources']]
        elif 'resource' in response_payload:
            return self._parse_response(response_payload['resource'], comment)
        else:
            return response_payload # Not sure what to do in this scenario or when it might occur

    def list(self):
        return self.make_request('list', '/')

    def create(self, data):
        return self.make_request('create', '/', data)

    def get(self, id):
        return self.make_request('get', '/' + id)

    def update(self, id, data):
        return self.make_request('update', '/' + id, data)

    def comment_get(self, id):
        return self.make_request('comment_get', '/' + id, comment=True)

    def comment_create(self, id, data):
        return self.make_request('comment_create', '/' + id, data, comment=True)
