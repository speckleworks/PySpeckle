import uuid
import pytest


@pytest.fixture(scope='module')
def resource():
    return {
        'role': 'Hybrid',
        'documentName': 'Test',
        'documentType': 'DataServer',
        'documentLocation': 'http://some.server.com',
        'documentGuid': 'some-long-uuid',
        'online': True,
    }


@pytest.fixture(scope='module')
def updated_resource():
    return {
        'documentName': 'Updated Test',
        'documentLocation': 'http://some.other.server.com',
    }

@pytest.fixture(scope='module')
def stream(client):
    stream = client.streams.create({
        'name': 'example stream',
        'description': 'a stream for testing purposes',
        'tags': [
            'test',
            'example'
        ],
        'commitMessage': 'created stream',
        'objects': [],
        'layers': [],
    })
    yield stream
    client.streams.delete(id=stream.streamId)

def test_list_none(client):
    data = client.api_clients.list()
    assert data == []


def test_create(client, resource, stream):
    resource['streamId'] = stream.streamId

    returned_resource = client.api_clients.create(resource)

    assert resource['role'] == returned_resource.role
    assert resource['documentName'] == returned_resource.documentName
    assert resource['documentType'] == returned_resource.documentType
    assert resource['documentLocation'] == returned_resource.documentLocation
    assert resource['documentGuid'] == returned_resource.documentGuid
    assert resource['streamId'] == returned_resource.streamId
    assert resource['online'] == returned_resource.online
    

@pytest.mark.dependency(depends=['test_create'])
def test_get(client, resource):
    data = client.api_clients.list()
    assert len(data) == 1
    returned_resource = client.api_clients.get(id=data[0].id)

    assert resource['role'] == returned_resource.role
    assert resource['documentName'] == returned_resource.documentName
    assert resource['documentType'] == returned_resource.documentType
    assert resource['documentLocation'] == returned_resource.documentLocation
    assert resource['documentGuid'] == returned_resource.documentGuid
    assert resource['online'] == returned_resource.online

@pytest.mark.dependency(depends=['test_get'])
def test_update(client, updated_resource):
    data = client.api_clients.list()
    assert len(data) == 1
    response = client.api_clients.update(id=data[0].id, data=updated_resource)

    assert response['message'] == 'Client updated following fields: documentName,documentLocation,documentGuid'

    returned_resource = client.api_clients.get(id=data[0].id)

    assert updated_resource['documentName'] == returned_resource.documentName
    assert updated_resource['documentLocation'] == returned_resource.documentLocation

@pytest.mark.dependency(depends=['test_create'])
def test_delete(client):
    data = client.api_clients.list()
    assert data != []
    for api_client in data:
        client.api_clients.delete(id=api_client.id)
    data = client.api_clients.list()
    assert data == []
