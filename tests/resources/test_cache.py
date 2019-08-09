import uuid
import pytest


def test_create(client, resource):
    returned_resource = client.streams.create(resource)

    assert resource['name'] == returned_resource.name
    assert resource['description'] == returned_resource.description
    assert resource['tags'] == returned_resource.tags
    assert resource['objects'] == returned_resource.objects
    assert resource['layers'] == returned_resource.layers

    assert returned_resource.streamId is not None

@pytest.fixture(scope='session')
def test_create():
    cache = SpeckleCache("test.db")
    conn = cache.try_connect()
    
    if not conn:
        conn = cache.create_database()
    try:
	    assert conn != None
    except AssertionError as e:
        raise e