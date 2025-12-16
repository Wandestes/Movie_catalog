# movie_service/tests/unit/test_repository_unit.py

import pytest
import movie_service.movies_repository as movie_repo
from unittest.mock import MagicMock, patch

# ІМПОРТ: Тепер ви викликаєте функції без префікса 'repo.'
from movie_service.movies_repository import (
    get_all_movies, get_movie_by_id, add_movie,
    update_movie, delete_movie # <--- ДОДАНО
)

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

# movie_service/tests/unit/test_repository_unit.py (ДОДАТИ В КІНЕЦЬ ФАЙЛУ)

@patch('movie_service.movies_repository.get_connection')
def test_update_movie_success(mock_get_connection, mock_cursor):
    """Тестуємо успішне оновлення фільму."""
    
    # 1. Налаштування Mock-об'єктів
    mock_conn = MagicMock()
    mock_cursor.rowcount = 1 # Імітуємо, що оновлено 1 рядок
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    movie_id = 1
    # Важливо: використовуємо структуру, як у вашій функції update_movie
    update_data = {"title": "Updated Title", "year": 2024, "genre": "Sci-Fi", "rating": 5.0, "description": "New Desc"} 

    # 2. Виклик функції
    result = update_movie(movie_id, update_data)

    # 3. Перевірки (Asserts)
    assert result is True
    mock_conn.commit.assert_called_once()
    
    # Перевіряємо, що запит сформовано коректно
    expected_sql = "UPDATE movies SET title=%s, year=%s, genre=%s, rating=%s, description=%s WHERE id=%s"
    expected_params = ('Updated Title', 2024, 'Sci-Fi', 5.0, 'New Desc', 1)

    mock_cursor.execute.assert_called_once_with(expected_sql, expected_params)


@patch('movie_service.movies_repository.get_connection')
def test_delete_movie_success(mock_get_connection, mock_cursor):
    """Тестуємо успішне видалення фільму."""
    
    # 1. Налаштування Mock-об'єктів
    mock_conn = MagicMock()
    mock_cursor.rowcount = 1 # Імітуємо, що видалено 1 рядок
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn
    
    movie_id = 1

    # 2. Виклик функції
    result = delete_movie(movie_id)

    # 3. Перевірки (Asserts)
    assert result is True
    mock_conn.commit.assert_called_once()
    
    expected_sql = "DELETE FROM movies WHERE id = %s"
    mock_cursor.execute.assert_called_once_with(expected_sql, (movie_id,))

@patch('movie_service.movies_repository.get_connection')
def test_search_movies_success(mock_get_connection, mock_cursor):
    """Тест успішного пошуку фільмів за title або description."""
    
    # --- НАЛАШТУВАННЯ MOCK-З'ЄДНАННЯ ---
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn
    # -----------------------------------
    
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'title': 'The Matrix', 'year': 1999, 'genre': 'Sci-Fi', 'rating': 5.0, 'description': 'Blue or Red pill'},
    ]
    query_term = "matrix"
    movies = movie_repo.search_movies(query_term)
    
    assert len(movies) == 1
    
    # Перевіряємо, що запит був викликаний коректно
    expected_sql_prefix = "SELECT * FROM movies WHERE LOWER(title) LIKE %s OR LOWER(description) LIKE %s"
    
    # Видаляємо пробіли та переноси рядків для порівняння, оскільки Python може їх змінювати
    called_sql = " ".join(mock_cursor.execute.call_args[0][0].split())
    
    # Ми очікуємо, що SQL містить обидва умови пошуку
    assert expected_sql_prefix in called_sql
    
    expected_params = (f"%{query_term}%", f"%{query_term}%")
    assert mock_cursor.execute.call_args[0][1] == expected_params