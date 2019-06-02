from speckle.base.resource import ResourceBase, ResourceBaseSchema
from typing import List, Optional


NAME = 'comments'
METHODS = ['list', 'get', 'update', 'assigned',
           'delete', 'comment_get', 'comment_create']




class Resource(ResourceBase):
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.schema = self.comment_schema

        self.method_dict.update({
            'assigned': {
                    'method': 'GET'
                }
        })

    def assigned(self):
        return self.make_request('assigned', '/assigned')
