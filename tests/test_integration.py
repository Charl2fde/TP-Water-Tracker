import pytest

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()

def test_request_log_form(client):
    response = client.get('/log')
    assert b'Log Activity' in response.data