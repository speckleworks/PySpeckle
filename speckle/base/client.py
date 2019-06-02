import requests
from speckle import resources

DEFAULT_SERVER = 'https://hestia.speckle.works/api'
DEFAULT_HOST = 'hestia.speckle.works'
DEFAULT_VERSION = 'v1'
TRANSFER_PROTOCOL = 'https'


class ClientBase():

    def __init__(self, host=DEFAULT_HOST, version=DEFAULT_VERSION, transfer_protocol=TRANSFER_PROTOCOL):
        self.server = '{}://{}/api/{}'.format(transfer_protocol, host, version)
        self.me = None
        self.s = requests.Session()
        self.verbose = False


    def register(self, email, password, company, name=None, surname=None):
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

    
