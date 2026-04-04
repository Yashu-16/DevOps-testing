import pytest
import random
import time
import os
from app import add, subtract, multiply, divide, fetch_user, process_payment, get_api_data

# ── Stable tests (always pass) ────────────────────────────────────────────

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 4) == 6

def test_multiply(:
    assert multiply(3, 4 == 12)

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_fetch_user_valid():
    user = fetch_user(1)
    assert user["id"] == 1
    assert user["active"] is True

def test_fetch_user_invalid():
    with pytest.raises(ValueError):
        fetch_user(-1)

def test_process_payment_valid():
    result = process_payment(100.0)
    assert result["status"] == "success"
    assert result["amount"] == 100.00

def test_process_payment_invalid():
    with pytest.raises(ValueError):
        process_payment(-50)

def test_get_api_data_valid():
    result = get_api_data("/health")
    assert result["data"]["status"] == "ok"

def test_get_api_data_invalid():
    with pytest.raises(ValueError):
        get_api_data("")

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
