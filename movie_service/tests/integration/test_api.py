# movie_service/tests/integration/test_api.py

import pytest
from movie_service.app import create_app
from unittest.mock import patch, MagicMock
# !!! КОРЕКТНИЙ ІМПОРТ !!!
from movie_service.validation import validate_movie_data 

@pytest.fixture
def mock_repo():
    """Створює Mock об'єкт, що імітує репозиторій у модулі routes."""
    # !!! МИ ПАТЧИМО РЕПОЗИТОРІЙ, ЯК ЙОГО БУЛО ІМПОРТОВАНО У routes.py
    with patch('movie_service.routes.movie_repo', autospec=True) as mock:
        # Налаштування за замовчуванням
        mock.add_movie.return_value = True
        mock.update_movie.return_value = True
        mock.delete_movie.return_value = True
        mock.get_all_movies.return_value = []
        # Налаштування, щоб update/delete не видавали 404, якщо вони успішні
        mock.get_movie_by_id.return_value = {"id": 1, "title": "Test"} 
        yield mock

@pytest.fixture
def client():
    """Створює тестовий клієнт Flask."""
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def populated_db_for_crud(mock_repo):
    """Фікстура для підготовки ID 1 до UPDATE/DELETE."""
    # Налаштування для тесту update_movie_success
    mock_repo.get_movie_by_id.return_value = {
        'id': 1, 'title': 'Old Title', 'year': 2000, 'genre': 'Action', 'rating': 3.0, 'description': 'Old Desc'
    }
    return 1 # ID фільму для роботи


# ----------------------------------------------------
# ІСНУЮЧІ ТЕСТИ
# ----------------------------------------------------

def test_get_movies_list_empty(client, mock_repo):
    """Тест, що перевіряє порожній список фільмів."""
    response = client.get('/api/v1/movies')
    assert response.status_code == 200
    assert response.get_json() == []

# Використовуємо patch для валідації, щоб не залежати від логіки валідації в цьому тесті.
@patch('movie_service.validation.validate_movie_data', return_value=(True, None)) 
def test_add_movie_success(mock_validate, client, mock_repo):
    """Тест POST ендпоінта для додавання фільму."""
    new_movie = {
        "title": "Test Movie", "year": 2024, "genre": "Test Genre", "rating": 5.0, "description": "A film for testing"
    }
    response = client.post('/api/v1/movies', json=new_movie)
    
    assert response.status_code == 201
    
    # Перевіряємо, що репозиторій був викликаний
    mock_repo.add_movie.assert_called_once_with(new_movie)

@patch('movie_service.validation.validate_movie_data', return_value=(True, None))
def test_update_movie_success(mock_validate, client, populated_db_for_crud, mock_repo):
    """Тестуємо успішне оновлення фільму через PUT-запит."""
    movie_id = populated_db_for_crud
    update_data = {"title": "New Updated Title", "year": 2024, "genre": "Sci-Fi", "rating": 4.5, "description": "New Updated Description"}

    response = client.put(f'/api/v1/movies/{movie_id}', json=update_data)
    
    assert response.status_code == 200
    assert "updated successfully" in response.json['message']
    
    mock_repo.update_movie.assert_called_once_with(movie_id, update_data)


@patch('movie_service.validation.validate_movie_data', return_value=(True, None))
def test_update_movie_not_found(mock_validate, client, mock_repo):
    """Тестуємо, що повертається 404, якщо фільм не знайдено."""
    mock_repo.update_movie.return_value = False 
    
    response = client.put('/api/v1/movies/999', json={"title": "A", "year": 2020, "genre": "B", "rating": 3.0, "description": "C"})
    
    assert response.status_code == 404
    assert "Movie not found" in response.json['error']


def test_delete_movie_success(client, populated_db_for_crud, mock_repo):
    """Тестуємо успішне видалення фільму через DELETE-запит."""
    movie_id = populated_db_for_crud
    
    response = client.delete(f'/api/v1/movies/{movie_id}')
    
    assert response.status_code == 200
    assert "deleted successfully" in response.json['message']
    
    mock_repo.delete_movie.assert_called_once_with(movie_id)


def test_delete_movie_not_found(client, mock_repo):
    """Тестуємо, що повертається 404, якщо фільм для видалення не знайдено."""
    mock_repo.delete_movie.return_value = False 
    
    response = client.delete('/api/v1/movies/999')
    
    assert response.status_code == 404
    assert "Movie not found" in response.json['error']

def test_search_movies_success(client, mock_repo):
    """Тест успішного пошуку фільмів через API з параметром query."""
    
    # 1. Налаштовуємо mock-об'єкт, який поверне репозиторій при пошуку
    search_results = [
        {'id': 1, 'title': 'Search Match', 'year': 2000, 'genre': 'Action', 'rating': 4.0, 'description': 'A quick find'},
    ]
    # Налаштовуємо mock_repo.search_movies
    mock_repo.search_movies.return_value = search_results

    # 2. Викликаємо GET-запит з параметром query
    response = client.get('/api/v1/movies?query=match')
    
    # 3. Перевірка
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Search Match'

    mock_repo.search_movies.assert_called_once_with('match')
    mock_repo.get_all_movies.assert_not_called()