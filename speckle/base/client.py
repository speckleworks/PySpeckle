"""Speckle Client documentation

The SpeckleClient class is used to manage authentication and dispatch
request to a given SpeckleServer.

Example:
    Instantiate a client to a given server and register/authenticate to it::

        from speckle import SpeckleApiClient

        client = SpeckleApiClient('myspeckle.speckle.works')

        client.register(
            email='test@test.com',
            password='Speckle<3Python',
            company='SnakeySnakes',
            name='Snakey',
            surname='Snake'
        )

        streams = client.streams.list()

For more detailed documentation on the inidividual resources available go  :doc:`here </client_api_ref>`

"""

import requests
from speckle import resources


class ClientBase():
    """Base class for http speckle client

    This class contains the basic properties required to register, authenticate and hold authentication
    credentials.

    """
    
    DEFAULT_HOST = 'hestia.speckle.works'
    DEFAULT_VERSION = 'v1'
    TRANSFER_PROTOCOL = 'https'


    def __init__(self, host=DEFAULT_HOST, version=DEFAULT_VERSION, transfer_protocol=TRANSFER_PROTOCOL):
        self.server = '{}://{}/api/{}'.format(transfer_protocol, host, version)
        self.me = None
        self.s = requests.Session()
        self.verbose = False


    def register(self, email, password, company, name=None, surname=None):
        """Register a new user to the speckle server

        After a user has registered, this function will log them in and save auth token credentials
        in the client object.
        
        Arguments:
            email {str} -- Email address of the new user, must not exist on the server
            password {str} -- Pretty self explanatory, must be at least 8 characters long
            company {str} -- Company the user is registering to speckle under
        
        Keyword Arguments:
            name {str} -- User name, server will default to 'Anonymous' if None (default: {None})
            surname {str} -- User surname, server will default to '' if None (default: {None})
        """

        r = self.s.post(
            self.server + '/accounts/register',
            json={
                'name': name,
                'surname': surname,
                'email': email,
                'password': password,
                'company': company
            })

        response = r.json()
        assert response['success'], response['message']

        self.login(email, password)


    def login(self, email, password):
        """Login user to speckle server
        
        After a user has logged in, this function will save auth token credentials
        in the client object.

        Arguments:
            email {str} -- Email address of the new user, must not exist on the server
            password {str} -- Pretty self explanatory, must be at least 8 characters long. Oh, must also be the user's actual password...
        """

        r = self.s.post(
            self.server + '/accounts/login',
            json={
                'email': email,
                'password': password
            })

        response = r.json()
        assert response['success'], response['message']
        
        self.me = r.json()['resource']
        self.s.headers.update({
            'content-type': 'application/json',
            'Authorization': self.me['token'],
        })

    

    def __getattr__(self, name):
        try:
            attr = getattr(resources, name)
            # setattr(self, name, attr.Resource(self.s, self.server))
            return attr.Resource(self.s, self.server, self.me)
            # return getattr(self, name)
        except:
            raise 'Method {} is not supported by SpeckleClient class'.format(name)

    
