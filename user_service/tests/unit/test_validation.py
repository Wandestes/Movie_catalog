import pytest
from user_service.validation import validate_user_data

def test_validate_user_data_success():
    """Test validation with valid input data."""
    data = {
        "username": "tester",
        "email": "test@example.com",
        "password": "password123"
    }
    is_valid, error = validate_user_data(data)
    assert is_valid is True
    assert error is None

def test_validate_user_data_invalid_email():
    """Test validation with an incorrect email format."""
    data = {
        "username": "tester",
        "email": "wrong-email",
        "password": "password123"
    }
    is_valid, error = validate_user_data(data)
    assert is_valid is False
    assert error == "Invalid email format"