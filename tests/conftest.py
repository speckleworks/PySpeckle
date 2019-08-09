import uuid
import pytest
from speckle.SpeckleClient import SpeckleApiClient
from speckle import SpeckleCache

@pytest.fixture(scope='session')
def host():
    return 'localhost:3000'

@pytest.fixture(scope='session')
def use_ssl():
    return False

@pytest.fixture(scope='session')
def admin_account():
    return {
        'name': 'Testy',
        'surname': 'McTestyFace',
        'company': 'Test Inc',
        'email': 'test@test.com',
        'password': 'supersecretpassword'
    }

@pytest.fixture(scope='session')
def client(host, use_ssl, admin_account):
    client = SpeckleApiClient(host=host, use_ssl=use_ssl)
    try:
        client.register(**admin_account)
    except AssertionError as e:
        if str(e) == 'Email taken. Please login. Thanks!':
            client.login(email=admin_account['email'], password=admin_account['password'])
        else:
            raise e
    
    return client

@pytest.fixture(scope='module')
def user_account(host, use_ssl, admin_account):
    client = SpeckleApiClient(
            host=host, use_ssl=use_ssl)

    account = {
        'name': 'Test_1',
        'surname': 'McTestyFace_1',
        'company': 'Test Inc_1',
        # Can't delete users on TearDown so have to create new on each time for local development
        'email': '{}@test_1.com'.format(str(uuid.uuid4())),
        'password': 'supersecretpassword'
    }

    client.register(**account)
    user = client.me

    return user
