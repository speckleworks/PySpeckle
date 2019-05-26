import requests
from speckle import resources

DEFAULT_SERVER = 'https://hestia.speckle.works/api'
DEFAULT_HOST = 'hestia.speckle.works'
DEFAULT_VERSION = 'v1'


class ClientBase():

    def __init__(self, host=DEFAULT_HOST, version=DEFAULT_VERSION):
        self.server = 'https://{}/api/{}'.format(host, version)
        self.me = None
        self.s = requests.Session()
        self.verbose = False


    def register(self, email, password):
        r = self.s.post(
            self.server + '/accounts/register',
            json={
                'email': email,
                'password': password
            })

        assert r.status_code == 200, 'Failed to authenticate'

        self.login(email, password)

    def login(self, email, password):
        r = self.s.post(
            self.server + '/accounts/login',
            json={
                'email': email,
                'password': password
            })

        assert r.status_code == 200, 'Failed to authenticate'

        self.me = r.json()['resource']
        self.s.headers.update({
            'content-type': 'application/json',
            'Authorization': self.me['token'],
        })

    

    def __getattr__(self, name):
        try:
            attr = getattr(resources, name)
            setattr(self, name, attr.Resource(self.s, self.server))
            return getattr(self, name)
        except:
            raise 'Method {} is not supported by SpeckleClient class'.format(name)

    
