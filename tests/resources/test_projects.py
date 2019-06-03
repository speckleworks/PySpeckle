import uuid
import pytest


@pytest.fixture(scope='module')
def resource():
    return {
        'name': 'test project',
        'description': 'a project made for testing purposes',
        'tags': [],
        'streams': [],
    }


@pytest.fixture(scope='module')
def updated_resource():
    return {
        'name': 'test project',
        'description': 'a project made for testing purposes',
        'tags': [],
        'streams': [],
    }


@pytest.fixture(scope='module')
def streams(client):
    stream_1 = client.streams.create({
        'name': 'example stream 1',
        })
    stream_2 = client.streams.create({
        'name': 'example stream 2',
        })
    yield [stream_1, stream_2]
    streams = client.streams.list()
    for stream in streams:
        client.streams.delete(id=stream.streamId)


@pytest.fixture(scope='module')
def created_item(client, resource):
    return client.projects.create(resource)
    

@pytest.fixture
def comment():
    return {
        'text': 'Wow this is an amazing resource!',
    }

def test_create(client, resource):
    created_item = client.projects.create(resource)

    assert resource['name'] == created_item.name
    assert resource['description'] == created_item.description
    assert resource['tags'] == created_item.tags
    assert resource['streams'] == created_item.streams

    assert created_item.id is not None


@pytest.mark.dependency(depends=['test_create'])
def test_list(client, resource):
    assert len(client.projects.list()) == 1
    client.projects.create(resource)
    assert len(client.projects.list()) == 2


@pytest.mark.dependency(depends=['test_create'])
def test_get(client, created_item):
    returned_resource = client.projects.get(id=created_item.id)

    assert created_item.id == returned_resource.id
    assert created_item.name == returned_resource.name
    assert created_item.description == returned_resource.description
    assert created_item.tags == returned_resource.tags
    assert created_item.streams == returned_resource.streams

@pytest.mark.dependency(depends=['test_get'])
def test_add_stream(client, created_item, streams):
    created_item.streams = []

    client.projects.add_stream(created_item.id, streams[0].streamId)
    project = client.projects.get(created_item.id)
    assert project.streams == [streams[0].streamId]

    client.projects.add_stream(created_item.id, streams[1].streamId)
    project = client.projects.get(created_item.id)
    assert project.streams == [streams[0].streamId, streams[1].streamId]


@pytest.mark.dependency(depends=['test_add_stream'])
def test_remove_stream(client, created_item, streams):
    project = client.projects.get(created_item.id)
    assert len(project.streams) == 2

    client.projects.remove_stream(project.id, streams[1].streamId)
    project = client.projects.get(created_item.id)

    assert project.streams == [streams[0].streamId]

@pytest.mark.dependency(depends=['test_create'])
def test_user_manipulation(client, created_item, user_account):
    project = client.projects.get(created_item.id)

    assert project.permissions.canRead == []
    assert project.permissions.canWrite == []

    client.projects.add_user(created_item.id, user_account['_id'])
    project = client.projects.get(created_item.id)

    assert project.canRead == [user_account['_id']]
    assert project.permissions.canWrite == [user_account['_id']]

    client.projects.downgrade_user(created_item.id, user_account['_id'])
    project = client.projects.get(created_item.id)

    assert project.canRead == [user_account['_id']]
    assert project.permissions.canWrite == []

    client.projects.upgrade_user(created_item.id, user_account['_id'])
    project = client.projects.get(created_item.id)

    assert project.canRead == [user_account['_id']]
    assert project.permissions.canWrite == [user_account['_id']]

    client.projects.remove_user(created_item.id, user_account['_id'])
    project = client.projects.get(created_item.id)

    assert project.canRead == []
    assert project.permissions.canWrite == []


@pytest.mark.dependency(depends=['test_create'])
def test_comments(client, created_item, comment):
    comments = client.projects.comment_get(created_item.id)
    assert comments == []
    client.projects.comment_create(created_item.id, comment)
    comments = client.projects.comment_get(created_item.id)
    assert len(comments) == 1
    assert comments[0].text == comment['text']


@pytest.mark.dependency(depends=['test_comments'])
def test_delete(client, resource):
    data = client.projects.list()
    assert data != []
    for project in data:
        client.projects.delete(id=project.id)
