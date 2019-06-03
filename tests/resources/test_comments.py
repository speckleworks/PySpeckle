import pytest


@pytest.fixture(scope='module')
def resource():
    return {
        'text': 'Wow this is an amazing comment!',
    }

@pytest.fixture
def comment():
    return {
        'text': 'Comments within comments... woah!',
    }


@pytest.fixture(scope='module')
def created_item(client, resource):
    project = client.projects.create({
        'name': 'test project',
        'description': 'a project made for testing purposes',
        'tags': [],
        'streams': [],
    })
    yield client.projects.comment_create(project.id, resource)
    client.projects.delete(project.id)

@pytest.mark.dependency()
def test_list(client, resource, created_item):
    # By this stage we should have created a bunch of comments
    initial_count = client.comments.list()
    assert len(initial_count) >= 1


@pytest.mark.dependency()
def test_get(client, created_item):
    returned_resource = client.comments.get(id=created_item.id)

    assert created_item.id == returned_resource.id
    assert created_item.text == returned_resource.text

@pytest.mark.dependency(depends=['test_get'])
def test_comments(client, created_item, comment):
    comments = client.comments.comment_get(created_item.id)
    assert comments == []
    client.comments.comment_create(created_item.id, comment)
    comments = client.comments.comment_get(created_item.id)
    assert len(comments) == 1
    assert comments[0].text == comment['text']


@pytest.mark.dependency(depends=['test_get'])
def test_assigned(client, created_item):
    assigned = client.comments.assigned()
    assert assigned == []
    created_item.assignedTo = [client.me['_id']]
    client.comments.update(created_item.id, created_item.dict())
    assigned = client.comments.assigned()
    assert len(assigned) == 1
    assert assigned[0].id == created_item.id

@pytest.mark.dependency(depends=['test_comments'])
def test_delete(client, resource):
    data = client.comments.list()
    assert data != []
    for comment in data:
        client.comments.delete(id=comment.id)
