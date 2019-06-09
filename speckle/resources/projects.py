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
    """Project Data Class
    
    Arguments:
        ResourceBaseSchema {BaseModel} -- The BaseModel for all Speckle objects
    """
    name: Optional[str]
    description: Optional[str]
    tags: List[str] = []
    streams: List[str] = []
    permissions: Optional[Permissions]


class Resource(ResourceBase):
    """API Access class for Projects

    """
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

    def list(self):
        """List all projects
        
        Returns:
            list -- A list of project data class instances
        """
        return self.make_request('list', '/')

    def create(self, data):
        """Create a project from a data dictionary
        
        Arguments:
            data {dict} -- A dictionary describing a project
        
        Returns:
            Project -- The instance created on the Speckle Server
        """
        return self.make_request('create', '/', data)

    def get(self, id):
        """Get a specific project from the SpeckleServer
        
        Arguments:
            id {str} -- The ID of the project to retrieve
        
        Returns:
            Project -- The project
        """
        return self.make_request('get', '/' + id)

    def update(self, id, data):
        """Update a specific project
        
        Arguments:
            id {str} -- The ID of the project to update
            data {dict} -- A dict of values to update
        
        Returns:
            dict -- a confirmation payload with the updated keys
        """
        return self.make_request('update', '/' + id, data)

    def delete(self, id):
        """Delete a specific project
        
        Arguments:
            id {str} -- The ID of the project to delete
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('delete', '/' + id)

    def comment_get(self, id):
        """Retrieve comments attached to a project
        
        Arguments:
            id {str} -- The ID of the project to retrieve comments from
        
        Returns:
            list -- A list of comments
        """
        return self.make_request('comment_get', '/' + id, comment=True)

    def comment_create(self, id, data):
        """Add a comment to a project
        
        Arguments:
            id {str} -- The ID of the project to comment on
            data {dict} -- A comment dictionary object
        
        Returns:
            CommentSchema -- The comment created by the server
        """
        return self.make_request('comment_create', '/' + id, data, comment=True)


    def add_stream(self, id, stream_id):
        """Add a Stream to a project
        
        Arguments:
            id {str} -- The ID of a project
            stream_id {str} -- The StreamId of a stream
        
        Returns:
            dict -- A dictionary with the stream and the project
        """
        return self.make_request('add_stream', '/' + id + '/addstream/' + stream_id)

    def remove_stream(self, id, stream_id):
        """Remove a stream from a project
        
        Arguments:
            id {str} -- The ID of a project
            stream_id {str} -- The StreamId of a stream
        
        Returns:
            dict -- A dictionary with the stream and the project
        """
        return self.make_request('remove_stream', '/' + id + '/removestream/' + stream_id)
    
    def add_user(self, id, user_id):
        """Add a user to a project.

        Note:
            When a user is first added to a project they have read and write
            authorizations. If you only want to allow them to write be sure to
            downgrade the user right after adding them.
        
        Arguments:
            id {str} -- The ID of a project
            user_id {str} -- The ID of a user
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('add_user', '/' + id + '/adduser/' + user_id)

    def remove_user(self, id, user_id):
        """Remove a user from a project

        Note:
            When you remove a user from a project this also removes all of their
            read and write access to the project's streams.
        
        Arguments:
            id {str} -- The ID of a project
            user_id {str} -- The ID of a user
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('remove_user', '/' + id + '/removeuser/' + user_id)

    def upgrade_user(self, id, user_id):
        """Upgrade a user to have Write access to the project and it's streams
        
        Arguments:
            id {str} -- The ID of a project
            user_id {str} -- The ID of a user
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('upgrade_user', '/' + id + '/upgradeuser/' + user_id)

    def downgrade_user(self, id, user_id):
        """Downgrade a user to have only Read access to the project and it's streams
        
        Arguments:
            id {str} -- The ID of a project
            user_id {str} -- The ID of a user
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('downgrade_user', '/' + id + '/downgradeuser/' + user_id)
