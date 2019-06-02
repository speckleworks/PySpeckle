from speckle.base.resource import ResourceBase
from pydantic import BaseModel
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema

NAME = 'projects'
METHODS = [
    'list', 'create', 'get', 'update', 'delete',
    'comment_get', 'comment_create', 'add_stream',
    'add_user', 'remove_user', 'remove_stream',
    'upgrade_user', 'downgrade_user'
    ]

class Permissions(BaseModel):
    canRead: Optional[List[str]]
    canWrite: Optional[List[str]]

class Project(ResourceBaseSchema):
    name: Optional[str]
    description: Optional[str]
    tags: List[str] = []
    streams: List[str] = []
    permissions: Optional[Permissions]


class Resource(ResourceBase):
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.method_dict.update({
            'add_stream': {
                'method': 'PUT'
            },
            'remove_stream': {
                'method': 'DELETE'
            },
            'add_user': {
                'method': 'PUT'
            },
            'remove_user': {
                'method': 'DELETE'
            },
            'upgrade_user': {
                'method': 'PUT'
            },
            'downgrade_user': {
                'method': 'PUT'
            },
        })

        self.schema = Project


    def add_stream(self, id, stream_id):
        return self.make_request('add_stream', '/' + id + '/addstream/' + stream_id)

    def remove_stream(self, id, stream_id):
        return self.make_request('remove_stream', '/' + id + '/removestream/' + stream_id)
    
    def add_user(self, id, user_id):
        return self.make_request('add_user', '/' + id + '/adduser/' + user_id)

    def remove_user(self, id, user_id):
        return self.make_request('remove_user', '/' + id + '/removeuser/' + user_id)

    def upgrade_user(self, id, user_id):
        return self.make_request('upgrade_user', '/' + id + '/upgradeuser/' + user_id)

    def downgrade_user(self, id, user_id):
        return self.make_request('downgrade_user', '/' + id + '/downgradeuser/' + user_id)
