import json
from requests import Request
from pydantic import BaseModel
from pydoc import locate
from typing import List, Optional
import dataclasses
from dataclasses import dataclass
from datetime import datetime

SCHEMAS = {}

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
        return [v for v in (clean_empty(v) for v in d) if v is not None]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v is not None}

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

    def _prep_request(self, method, path, comment, data, params):
        assert method in self.methods, 'method {} not supported for {} calls'.format(method, self.name)

        if comment:
            url = self._comment_path + path
            if data:
                dataclass_instance = self.comment_schema.parse_obj(data)
                data = clean_empty(dataclass_instance.dict(by_alias=True))
        else:
            url = self._path + path
            if data:
                if isinstance(data, list):
                    data_list = []
                    if self.schema:
                        for d in data:
                            if isinstance(d, dict):
                                dataclass_instance = self.schema.parse_obj(d)
                                data_list.append(clean_empty(dataclass_instance.dict(by_alias=True)))
                            elif isinstance(d, str):
                                data_list.append(d)
                        data = data_list
                elif self.schema:
                    if isinstance(data, dict):
                        dataclass_instance = self.schema.parse_obj(data)
                    else:
                        dataclass_instance = data
                    data = clean_empty(dataclass_instance.dict(by_alias=True))
        return self.s.prepare_request(Request(self.method_dict[method]['method'], url, json=data, params=params))

    def _parse_response(self, response, comment=False, schema=None):
        """Parse the request response

        Arguments:
            response {Response} -- A response from the server
            comment {bool} -- Whether or not the response is a comment
            schema {Schema} -- Optional schema to parse the response with

        Returns:
            Schema / dict -- An object derived from SpeckleObject if possible, otherwise 
            a dict of the response resource
        """
        if schema:
            # If a schema is defined, then try to parse it with that
            return schema.parse_obj(response)
        elif comment:
            return self.comment_schema.parse_obj(response)
        elif 'type' in response:
            # Otherwise, check if the incoming type is within the dict of loaded schemas
            types = response['type'].split('/')
            for t in reversed(types):
                if t in SCHEMAS:
                    return SCHEMAS[t].parse_obj(response)
        if self.schema:
            return self.schema.parse_obj(response)
        return response


    def make_request(self, method, path, data=None, comment=False, schema=None, params=None):
        r = self._prep_request(method, path, comment, data, params)
        resp = self.s.send(r)
        resp.raise_for_status()
        response_payload = resp.json()
        assert response_payload['success'] == True, json.dumps(response_payload)

        if 'resources' in response_payload:
            return [self._parse_response(resource, comment, schema) for resource in response_payload['resources']]
        elif 'resource' in response_payload:
            return self._parse_response(response_payload['resource'], comment, schema)
        else:
            return response_payload # Not sure what to do in this scenario or when it might occur