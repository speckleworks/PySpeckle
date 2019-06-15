from speckle.base.resource import ResourceBase, ResourceBaseSchema
from typing import List, Optional


NAME = 'comments'
METHODS = ['list', 'get', 'update', 'assigned',
           'delete', 'comment_get', 'comment_create']


class Resource(ResourceBase):
    """API Access class for Comments

    """

    def __init__(self, session, basepath, me):
        super().__init__(session, basepath, me, NAME, METHODS)

        self.schema = self.comment_schema

        self.method_dict.update({
            'assigned': {
                    'method': 'GET'
                }
        })

    def list(self):
        """List all comments
        
        Returns:
            list -- A list of comment data class instances
        """
        return self.make_request('list', '/')


    def get(self, id):
        """Get a specific comment from the SpeckleServer
        
        Arguments:
            id {str} -- The ID of the comment to retrieve
        
        Returns:
            Comment -- The comment
        """
        return self.make_request('get', '/' + id)

    def update(self, id, data):
        """Update a specific comment
        
        Arguments:
            id {str} -- The ID of the comment to update
            data {dict} -- A dict of values to update
        
        Returns:
            dict -- a confirmation payload with the updated keys
        """
        return self.make_request('update', '/' + id, data)

    def delete(self, id):
        """Delete a specific comment
        
        Arguments:
            id {str} -- The ID of the comment to delete
        
        Returns:
            dict -- A confirmation payload
        """
        return self.make_request('delete', '/' + id)

    def comment_get(self, id):
        """Retrieve comments attached to a comment
        
        Arguments:
            id {str} -- The ID of the comment to retrieve comments from
        
        Returns:
            list -- A list of comments
        """
        return self.make_request('comment_get', '/' + id, comment=True)

    def comment_create(self, id, data):
        """Add a comment to a comment
        
        Arguments:
            id {str} -- The ID of the comment to comment on
            data {dict} -- A comment dictionary object
        
        Returns:
            Comment -- The comment created by the server
        """
        return self.make_request('comment_create', '/' + id, data, comment=True)

    def assigned(self):
        """Get the list of all comments where the logged in user is assigned
        
        Returns:
            list -- A list of comments the user is assigned to
        """
        return self.make_request('assigned', '/assigned')
