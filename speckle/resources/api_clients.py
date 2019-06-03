import uuid
from speckle.base.resource import ResourceBase
from pydantic import BaseModel, UUID4, validator
from typing import List, Optional, Union
from speckle.base.resource import ResourceBase, ResourceBaseSchema
from speckle.resources.accounts import User
from enum import Enum

NAME = 'clients'
METHODS = ['list', 'create', 'get', 'update',
           'delete']


class RoleEnum(str, Enum):
    receiver: 'Receiver'
    sender: 'Sender'
    hybrid: 'Hybrid'


class ApiClient(ResourceBaseSchema):
    # role: Optional[RoleEnum] = RoleEnum.receiver
    role: Optional[str]
    documentName: Optional[str]
    documentType: Optional[str]
    documentLocation: Optional[str]
    documentGuid: Optional[str]
    streamId: Optional[str]
    online: Optional[bool]
    owner: Optional[Union[User, str]]

    @validator('documentGuid', pre=True, always=True)
    def set_guid(cls, v):
        return v or str(uuid.uuid4())

class Resource(ResourceBase):
    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.schema = ApiClient
