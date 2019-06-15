import json
from requests import Request
from pydantic import BaseModel
from typing import List, Optional
import dataclasses
from dataclasses import dataclass
from datetime import datetime

class ResourceBaseSchema(BaseModel):
    id: Optional[str]
    private: Optional[bool]
    canRead: Optional[List[str]]
    canWrite: Optional[List[str]]
    owner: Optional[str]
    anonymousComments: Optional[bool]
    comments: Optional[List[str]]
    createdAt: Optional[str]
    updatedAt: Optional[str]

    class Config:
        fields = {'id': '_id'}

class ResourceInfo(BaseModel):
    resourceType: str
    resourceId: str

class Comment(BaseModel):
    id: Optional[str]
    owner: Optional[str]
    comments: Optional[List[str]]
    text: Optional[str]
    flagged: Optional[bool]
    resource: Optional[ResourceInfo]
    otherResources: Optional[List[ResourceInfo]]
    closed: Optional[bool]
    assignedTo: Optional[List[str]]
    labels: Optional[List[str]]
    priority: Optional[str]
    status: Optional[str]
    view: Optional[dict]
    screenshot: Optional[str]

    class Config:
        fields = {'id': '_id'}


def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

class ResourceBase(object):

    def __init__(self, session, basepath, me, name, methods):
        self.s = session
        self._path = basepath + '/' + name
        self.me = me
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

    def _parse_response(self, response, comment=False, schema=None):
        if schema:
            return schema.parse_obj(response)
        elif comment:
            return self.comment_schema.parse_obj(response)
        elif self.schema:
            return self.schema.parse_obj(response)
        else:
            return response


    def make_request(self, method, path, data=None, comment=False, schema=None):
        r = self._prep_request(method, path, comment, data)
        resp = self.s.send(r)

        response_payload = resp.json()
        print(json.dumps(response_payload, indent=2))

        assert response_payload['success'] == True, json.dumps(response_payload)
        # print(response_payload)
        if 'resources' in response_payload:
            return [self._parse_response(resource, comment, schema) for resource in response_payload['resources']]
        elif 'resource' in response_payload:
            return self._parse_response(response_payload['resource'], comment, schema)
        else:
            return response_payload # Not sure what to do in this scenario or when it might occur
