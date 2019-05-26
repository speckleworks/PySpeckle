import uuid
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, UUID4, validator
from typing import List, Optional
from speckle.base.resource import ResourceBase, ResourceBaseSchema
from enum import Enum

NAME = 'clients'
METHODS = ['list', 'create', 'get', 'update',
           'delete']


class RoleEnum(str, Enum):
    Receiver: 'Receiver'
    Sender: 'Sender'
    Hybrid: 'Hybrid'


class Client(ResourceBaseSchema):
    role: Optional[RoleEnum]
    documentName: Optional[str]
    documentType: Optional[str]
    documentLocation: Optional[str]
    documentGuid: Optional[UUID4]
    streamId: Optional[str]
    online: Optional[bool]

    @validator('documentGuid', pre=True, always=True)
    def set_guid(cls, v):
        return v or uuid.uuid4()

class Resource(ResourceBase):
    def __init__(self, session, basepath):
        super().__init__(session, basepath, NAME, METHODS)

        self.schema = Client
