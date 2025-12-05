# db/movies_repository.py

from db.connection import get_connection

def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies

def search_movies(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM movies WHERE LOWER(title) LIKE %s",
        (f"%{query.lower()}%",)
    )
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies

def get_movie_by_id(movie_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    cursor.close()
    conn.close()
    return movie

def add_movie(movie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO movies (title, year, genre, rating, description)
           VALUES (%s, %s, %s, %s, %s)""",
        (movie["title"], movie["year"], movie["genre"], movie["rating"], movie["description"])
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_movie(movie_id, movie):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE movies SET title=%s, year=%s, genre=%s, rating=%s, description=%s 
           WHERE id=%s""",
        (movie["title"], movie["year"], movie["genre"], movie["rating"], movie["description"], movie_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
