import pytest
from movie_service.validation import validate_movie_data

# Базовий коректний об'єкт для використання у тестах
VALID_MOVIE = {
    "title": "Inception",
    "year": 2010,
    "genre": "Sci-Fi",
    "rating": 4.8,
    "description": "Dream-within-a-dream heist movie."
}

def test_validation_success():
    """Перевірка, що коректні дані проходять валідацію."""
    is_valid, msg = validate_movie_data(VALID_MOVIE)
    assert is_valid is True
    assert msg == ""

@pytest.mark.parametrize("field_to_remove, expected_message", [
    ('title', "Missing required field: 'title'"),
    ('year', "Missing required field: 'year'"),
    ('rating', "Missing required field: 'rating'"),
])
def test_validation_missing_required_fields(field_to_remove, expected_message):
    """Перевірка помилок, коли відсутні обов'язкові поля."""
    invalid_data = VALID_MOVIE.copy()
    del invalid_data[field_to_remove]
    
    is_valid, msg = validate_movie_data(invalid_data)
    assert is_valid is False
    assert expected_message in msg

@pytest.mark.parametrize("invalid_year, expected_message", [
    ("2010", "Year must be a valid integer (e.g., 2024)."), # Рядок замість int
    (1800, "Year must be a valid integer (e.g., 2024)."),    # Занадто старий рік
    (None, "Year must be a valid integer (e.g., 2024)."),    # None
])
def test_validation_invalid_year(invalid_year, expected_message):
    """Перевірка помилок для некоректного поля 'year'."""
    invalid_data = VALID_MOVIE.copy()
    invalid_data['year'] = invalid_year
    
    is_valid, msg = validate_movie_data(invalid_data)
    assert is_valid is False
    assert expected_message in msg

@pytest.mark.parametrize("invalid_rating, expected_message", [
    (5.1, "Rating must be a number between 0.0 and 5.0."),    # Занадто високий
    (-0.1, "Rating must be a number between 0.0 and 5.0."),   # Занадто низький
    ("5", "Rating must be a number between 0.0 and 5.0."),    # Рядок замість number
])
def test_validation_invalid_rating(invalid_rating, expected_message):
    """Перевірка помилок для некоректного поля 'rating'."""
    invalid_data = VALID_MOVIE.copy()
    invalid_data['rating'] = invalid_rating
    
    is_valid, msg = validate_movie_data(invalid_data)
    assert is_valid is False
    assert expected_message in msg

def test_validation_empty_title():
    """Перевірка, що порожня назва не проходить валідацію."""
    invalid_data = VALID_MOVIE.copy()
    invalid_data['title'] = "  "
    
    is_valid, msg = validate_movie_data(invalid_data)
    assert is_valid is False
    assert "Title must be a non-empty string." in msg