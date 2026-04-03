import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    """Test the main route returns correct response."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Hello World!'
    assert data['status'] == 'success'
    assert 'timestamp' in data

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert data['version'] == '1.0.0'

def test_get_data(client):
    """Test the data API endpoint."""
    response = client.get('/api/data')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'users' in data
    assert 'total_count' in data
    assert len(data['users']) == 2
    assert data['total_count'] == 2
    
    # Test user structure
    user = data['users'][0]
    assert 'id' in user
    assert 'name' in user
    assert 'email' in user

def test_invalid_route(client):
    """Test that invalid routes return 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404