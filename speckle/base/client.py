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
from websocket import WebSocketApp
import urllib

class ClientBase():
    """Base class for http speckle client

    This class contains the basic properties required to register, authenticate and hold authentication
    credentials.

    """
    
    DEFAULT_HOST = 'hestia.speckle.works'
    DEFAULT_VERSION = 'v1'
    USE_SSL = True

    def __init__(self, host=DEFAULT_HOST, version=DEFAULT_VERSION, use_ssl=USE_SSL, verbose=False):

        ws_protocol = 'ws'
        http_protocol = 'http'

        if use_ssl:
            ws_protocol = 'wss'
            http_protocol = 'https'

        self.websockets_server = '{}://{}'.format(ws_protocol, host)
        self.server = '{}://{}/api/{}'.format(http_protocol, host, version)
        self.me = None
        self.s = requests.Session()
        self.verbose = verbose


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
        if self.verbose:
            print(response)
        assert response['success'], response['message']
        
        self.me = r.json()['resource']
        self.s.headers.update({
            'content-type': 'application/json',
            'Authorization': self.me['token'],
        })

    def websockets(self, stream_id, client_id=None, header=None,
                   on_open=None, on_message=None, on_error=None,
                   on_close=None, on_ping=None, on_pong=None,
                   on_cont_message=None, get_mask_key=None,
                   subprotocols=None, on_data=None):
        """Connect to a specific stream on the host server through websockets
        
        This function essentially generates the correct connection url the Speckle Server
        expects in order to connect to a specific stream. After that all this function does
        is instantiate a WebScoketApp class from the `websocket-client <https://github.com/websocket-client/websocket-client>`_
        package.

        Arguments:
            stream_id {str} -- The id of a stream (stream.streamId)
        
        Keyword Arguments:
            client_id {str} -- The id of the client to authenticate as (default: {None})
            header {dict} -- custom header for websocket handshake (default: {None})
            on_open {function} -- callable object which is called at opening websocket. (default: {None})
                This function takes 1 argument:
                1. this class object
            on_close {function} -- callable object which is called when closed the connection (default: {None})
                This function takes 1 argument:
                1. this class object
            on_message {function} -- callable object which is called when receiving data (default: {None})
                This function takes 2 arguments:
                1. this class object
                2. the utf-8 string sent by the server
            on_error {function} -- callable object which is called when an error is sent by the server (default: {None})
                This function takes 2 arguments:
                1. this class object
                2. an exception object
            on_ping {function} -- callable object which is called when the server pings (default: {None})
                This function takes 2 arguments:
                1. this class object
                2. the utf-8 string sent by the server
            on_pong {function} -- callable object which is called when the server pings (default: {None})
                This function takes 2 arguments:
                1. this class object
                2. the utf-8 string sent by the server
            on_cont_message {function} -- callback object which is called when receive continued frame data. (default: {None})
                This function takes 2 arguments:
                1. this class object
                2. the utf-8 string sent by the server
                3. is continue flag, if 0 the data continues to the next frame
            on_data {function} -- callback object which is called when a message received (default: {None})
                This is called before on_message or on_cont_message,
                and then on_message or on_cont_message is called.
                on_data has 4 argument.
                1. this class object.
                2. the utf-8 string sent by the server
                3. data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be same.
                4. continue flag. if 0, the data continue
            get_mask_key {function} -- a callable to produce new mask keys (default: {None})
                see the WebSocket.set_mask_key's docstring for more information
            subprotocols {list} -- list of available sub protocols (default: {None})
        
        Returns:
            WebSocketApp -- a websocket-client instance


        Example:
            .. code-block:: python

                from speckle import SpeckleApiClient

                host = 'hestia.speckle.works'
                stream_id = 'MawOwhxET'

                client = SpeckleApiClient(host=host)
                client.login('test@test.com', 'testestestest')

                def print_message(ws, message):
                    print(message)


                ws = client.websockets(stream_id, on_message=print_message)

                # Send a message to the stream
                ws.send('Hi Speckle!!!')

                # Start a listening server that will print what ever message
                # is sent to it (due to the print_message function defined above)
                ws.run_forever()
        """
        
        if not client_id:
            api_client = self.api_clients.create({
                'streamId': stream_id
            })

            client_id = api_client.id

        params = {
            'client_id': client_id,
            'access_token': self.me['token'],
            'stream_id': stream_id
        }

        url = '{}?{}'.format(
            self.websockets_server,
            urllib.parse.urlencode(params)
        )
        return WebSocketApp(
            url,
            header,
            on_open,
            on_message,
            on_error,
            on_close,
            on_ping,
            on_pong,
            on_cont_message,
            get_mask_key,
            subprotocols,
            on_data,
        )


    def __getattr__(self, name):
        try:
            attr = getattr(resources, name)
            return attr.Resource(self.s, self.server, self.me)
        except:
            raise Exception('Method {} is not supported by SpeckleClient class'.format(name))

    
