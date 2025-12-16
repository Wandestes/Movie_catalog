# movie_service/tests/unit/test_repository_unit.py

import pytest
from unittest.mock import MagicMock, patch

# ІМПОРТ: Тепер ви викликаєте функції без префікса 'repo.'
from movie_service.movies_repository import (
    get_all_movies, get_movie_by_id, add_movie
)
# ВИДАЛЕНО: from movie_service import connection

# Фікстура, яка імітує об'єкт курсора з даними
@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    # Імітуємо повернення даних для FetchOne
    cursor.fetchone.return_value = {
        "id": 1,
        "title": "Mock Movie",
        "rating": 5.0
    }
    # Імітуємо повернення даних для FetchAll
    cursor.fetchall.return_value = [
        {"id": 1, "title": "Movie 1"},
        {"id": 2, "title": "Movie 2"}
    ]
    return cursor

# Фікстура, яка імітує підключення до бази даних
# ВИПРАВЛЕНО ШЛЯХ MOCKING: Патчимо там, де функція використовується (в репозиторії)
@patch('movie_service.movies_repository.get_connection')
def test_get_all_movies_success(mock_get_connection, mock_cursor):
    """Тестуємо успішне отримання всіх фільмів."""

    # 1. Налаштування Mock-об'єктів
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    # 2. Виклик функції, яку тестуємо
    movies = get_all_movies()

    # 3. Перевірки (Asserts)

    # ПЕРЕВІРКА SQL: Чи був викликаний правильний SQL-запит?
    mock_cursor.execute.assert_called_once_with("SELECT * FROM movies")

    # ПЕРЕВІРКА РЕЗУЛЬТАТУ: Чи повернулися імітовані дані?
    assert len(movies) == 2
    assert movies[0]['title'] == "Movie 1"

    # ПЕРЕВІРКА ЗАКРИТТЯ: Чи було закрито курсор і з'єднання?
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('movie_service.movies_repository.get_connection')
def test_get_movie_by_id_found(mock_get_connection, mock_cursor):
    """Тестуємо успішне отримання фільму за ID."""

    # 1. Налаштування Mock-об'єктів
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    # 2. Виклик функції
    movie_id = 1
    movie = get_movie_by_id(movie_id)

    # 3. Перевірки (Asserts)

    # ПЕРЕВІРКА SQL: Перевіряємо параметри запиту
    expected_sql = "SELECT * FROM movies WHERE id = %s"
    mock_cursor.execute.assert_called_once_with(expected_sql, (movie_id,))

    # ПЕРЕВІРКА РЕЗУЛЬТАТУ
    assert movie['id'] == 1
    assert movie['title'] == "Mock Movie"


@patch('movie_service.movies_repository.get_connection')
def test_add_movie_success(mock_get_connection, mock_cursor): # ДОДАЄМО mock_cursor СЮДИ
    """Тестуємо успішне додавання нового фільму."""

    # Налаштування Mock-об'єктів
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    new_movie = {
        "title": "New Film",
        "year": 2024,
        "genre": "Action",
        "rating": 4.5,
        "description": "Test film"
    }

    # Виклик функції
    result = add_movie(new_movie)

    # Перевірка
    assert result is True

    # ПЕРЕВІРКА КОМІТУ: Чи був викликаний commit()
    mock_conn.commit.assert_called_once()

    # ПЕРЕВІРКА SQL: Перевіряємо, чи був виконаний INSERT
    mock_cursor.execute.assert_called_once()

# --- ДОДАТКОВИЙ ТЕСТ: ОБРОБКА ПОМИЛОК ---

@patch('movie_service.movies_repository.get_connection')
def test_get_all_movies_db_connection_fail(mock_get_connection):
    """Тестуємо, що повертається порожній список, якщо підключення до БД не вдалося."""

    # Налаштування: імітуємо, що підключення повернуло None
    mock_get_connection.return_value = None

    # Виклик функції
    movies = get_all_movies()

    # Перевірки
    assert movies == []