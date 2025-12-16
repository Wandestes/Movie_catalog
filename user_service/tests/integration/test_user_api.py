import pytest
from movie_service.app import create_app
from unittest.mock import patch

@pytest.fixture
def client():
    """Setup Flask test client."""
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

@patch('user_service.routes.user_repo.create_user')
def test_add_user_api_success(mock_create, client):
    """Test user creation via API."""
    mock_create.return_value = 1
    
    payload = {
        "username": "tester",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post('/api/v1/users', json=payload)
    
    # Check if the route exists (not 404)
    assert response.status_code == 201
    assert response.json['id'] == 1

@patch('user_service.routes.user_repo.get_user_by_id')
def test_get_user_api_not_found(mock_get, client):
    """Test user not found scenario."""
    mock_get.return_value = None
    
    response = client.get('/api/v1/users/999')
    
    assert response.status_code == 404
    # Ensure we got a JSON response, not an HTML error page
    assert response.is_json
    assert response.json['error'] == "User not found"