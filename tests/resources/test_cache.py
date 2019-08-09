import uuid
import pytest

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