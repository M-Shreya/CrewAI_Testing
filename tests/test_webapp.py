
import pytest
from testing.target.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert b"login" in response.data

def test_login_success(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'secret'})
    assert b'Success' in response.data

def test_login_failure(client):
    response = client.post('/login', data={'username': 'wrong', 'password': 'wrong'})
    assert b'Failure' in response.data