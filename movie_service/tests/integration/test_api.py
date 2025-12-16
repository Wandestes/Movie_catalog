import pytest
from movie_service.app import create_app
from unittest.mock import patch, MagicMock
from movie_service import connection

# Цю фікстуру ми залишаємо для загального клієнта (вона імітує cursor.fetchall = [])
# movie_service/tests/integration/test_api.py

@pytest.fixture
def mock_db_connection():
    """Створює об'єкт Mock для з'єднання з БД."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Патчимо get_connection під час виконання фікстури
    with patch('movie_service.movies_repository.get_connection', return_value=mock_conn) as mock_get_conn:
        yield mock_get_conn

@pytest.fixture
def client(mock_db_connection): # Приймаємо Mock як залежність
    """Створює тестовий клієнт Flask."""
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        # Передаємо Mock для доступу в тестах
        client.mock_get_connection = mock_db_connection
        yield client

def test_get_movies_list_empty(client):
    """Тест, що перевіряє порожній список фільмів."""
    response = client.get('/api/v1/movies')
    assert response.status_code == 200
    assert response.get_json() == []

# --- ВИПРАВЛЕННЯ `test_add_movie_success` ---
def test_add_movie_success(client):
    """Тест POST ендпоінта для додавання фільму."""
    new_movie = {
        "title": "Test Movie",
        "year": 2024,
        "genre": "Test Genre",
        "rating": 5.0,
        "description": "A film for testing"
    }
    
    # Виклик POST ендпоінта
    response = client.post('/api/v1/movies', json=new_movie)
    
    # 1. Перевірка статусу POST
    assert response.status_code == 201
    
    # 2. Доступ до об'єкта Mock:
    # Отримуємо мок-об'єкт з'єднання з фікстури.
    mock_get_connection = client.mock_get_connection
    mock_conn = mock_get_connection.return_value 
    
    # 3. Перевірка логіки репозиторію: Чи був викликаний commit()
    mock_conn.commit.assert_called_once()
    
    # 4. Перевірка, що було викликано INSERT запит (опціонально, але гарна практика)
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.assert_called_once() 