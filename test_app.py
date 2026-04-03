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
    """Test the hello world endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['message'] == 'Hello, World!'
    assert data['status'] == 'success'
    assert 'version' in data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'flask-app'


def test_process_data_valid(client):
    """Test processing valid data."""
    test_data = {'name': 'John Doe'}
    response = client.post('/api/data',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['processed'] is True
    assert data['original']['name'] == 'John Doe'
    assert data['name_length'] == 8


def test_process_data_no_data(client):
    """Test processing request with no data."""
    response = client.post('/api/data',
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_process_data_missing_name(client):
    """Test processing data without required name field."""
    test_data = {'age': 30}
    response = client.post('/api/data',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Missing required field: name'
