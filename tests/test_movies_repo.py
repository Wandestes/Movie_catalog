import mysql.connector
import pytest
from db.connection import get_connection
from db.movies_repository import (
    add_movie, get_all_movies, get_movie_by_id,
    update_movie, delete_movie
)

@pytest.fixture(scope="module")
def setup_test_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies_test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            year INT,
            genre VARCHAR(100),
            rating FLOAT,
            description TEXT
        );
    """)

    cursor.execute("DELETE FROM movies_test;")
    conn.commit()

    yield

    cursor.execute("DROP TABLE movies_test;")
    conn.commit()
    cursor.close()
    conn.close()


def test_add_movie(setup_test_table, monkeypatch):
    monkeypatch.setattr("db.movies_repository.TABLE_NAME", "movies_test")

    movie = {
        "title": "Test Movie",
        "year": 2020,
        "genre": "Test",
        "rating": 9.0,
        "description": "Test desc"
    }

    add_movie(movie)
    movies = get_all_movies()

    assert len(movies) == 1
    assert movies[0]['title'] == "Test Movie"


def test_get_movie_by_id(setup_test_table, monkeypatch):
    monkeypatch.setattr("db.movies_repository.TABLE_NAME", "movies_test")

    movie = get_movie_by_id(1)

    assert movie is not None
    assert movie['id'] == 1
    assert movie['title'] == "Test Movie"


def test_update_movie(setup_test_table, monkeypatch):
    monkeypatch.setattr("db.movies_repository.TABLE_NAME", "movies_test")

    updated = {
        "title": "Updated",
        "year": 2000,
        "genre": "Drama",
        "rating": 7.5,
        "description": "Updated text"
    }

    update_movie(1, updated)
    movie = get_movie_by_id(1)

    assert movie['title'] == "Updated"
    assert movie['rating'] == 7.5


def test_delete_movie(setup_test_table, monkeypatch):
    monkeypatch.setattr("db.movies_repository.TABLE_NAME", "movies_test")

    delete_movie(1)
    movie = get_movie_by_id(1)

    assert movie is None
