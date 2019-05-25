from speckle.base.resource import ResourceBase, ResourceBaseSchema
from typing import List, Optional


NAME = 'comments'
METHODS = ['list', 'create', 'get', 'update',
           'delete', 'comment_get', 'comment_create']




class Resource(ResourceBase):
    def __init__(self, session, basepath):
        super().__init__(session, basepath, NAME, METHODS)

        self.schema = self.comment_schema