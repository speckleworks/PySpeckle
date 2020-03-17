import uuid
import pytest


@pytest.fixture(scope='module')
def resource():
    return {
        'name': 'example stream',
        'description': 'a stream for testing purposes',
        'tags': [
            'test',
            'example'
        ],
        'commitMessage': 'created stream',
        'objects': [],
        'layers': [],
    }


@pytest.fixture(scope='module')
def updated_resource():
    return {
        'name': 'updated stream',
        'description': 'a stream for testing purposes',
        'tags': [
            'test',
            'example'
        ],
        'commitMessage': 'created stream',
        'objects': [],
        'layers': [],
    }


@pytest.fixture(scope='module')
def created_item(client, resource):
    return client.streams.create(resource)


@pytest.fixture
def comment():
    return {
        'text': 'Wow this is an amazing resource!',
    }

@pytest.fixture()
def api_client(client, created_item):
    api_client_dict = {
        'role': 'Hybrid',
        'documentName': 'Test',
        'documentType': 'DataServer',
        'documentLocation': 'http://some.server.com',
        'documentGuid': 'some-long-uuid',
        'online': True,
        'streamId': created_item.streamId
    }
    api_client = client.api_clients.create(api_client_dict)
    yield api_client
    client.api_clients.delete(api_client.id)

def test_create(client, resource):
    returned_resource = client.streams.create(resource)

    assert resource['name'] == returned_resource.name
    assert resource['description'] == returned_resource.description
    assert resource['tags'] == returned_resource.tags
    assert resource['objects'] == returned_resource.objects
    assert resource['layers'] == returned_resource.layers

    assert returned_resource.streamId is not None


@pytest.mark.dependency(depends=['test_create'])
def test_list(client, created_item):
    streams = client.streams.list()

    assert len(streams) == 2


@pytest.mark.dependency(depends=['test_create'])
def test_get(client, created_item):
    stream = client.streams.get(created_item.streamId)

    assert stream.id == created_item.id


@pytest.mark.dependency(depends=['test_create'])
def test_clone(client, created_item):
    clone, parent = client.streams.clone(created_item.streamId, 'cloned_stream')
    
    assert clone.name == 'cloned_stream'
    assert parent.name == created_item.name

    assert clone.parent == parent.streamId
    assert parent.children == [clone.streamId]


@pytest.mark.dependency(depends=['test_create'])
def test_list_clients_empty(client, created_item):
    api_clients = client.streams.list_clients(created_item.streamId)

    assert api_clients == []


@pytest.mark.dependency(depends=['test_create'])
def test_list_clients(client, created_item, api_client):
    api_clients = client.streams.list_clients(created_item.streamId)

    assert api_clients[0].id == api_client.id

def test_list_objects(client):
    # TODO(): add list objects test
    pass


def test_diff(client):
    # TODO(): add diff streams
    pass


@pytest.mark.dependency(depends=['test_create'])
def test_comments(client, created_item, comment):
    comments = client.streams.comment_get(created_item.streamId)
    assert comments == []
    client.streams.comment_create(created_item.streamId, comment)
    comments = client.streams.comment_get(created_item.streamId)
    assert len(comments) == 1
    assert comments[0].text == comment['text']

# @pytest.mark.dependency(depends=['test_create'])
# def test_delete(client, resource):
#     data = client.streams.list()
#     assert data != []
#     for stream in data:
#         client.streams.delete(id=stream.streamId)
