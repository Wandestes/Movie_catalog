# db/movies_repository.py
from db.connection import get_connection


TABLE_NAME = "movies" 

def get_all_movies():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies

def search_movies(query):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        f"SELECT * FROM {TABLE_NAME} WHERE LOWER(title) LIKE %s",
        (f"%{query.lower()}%",)
    )
    
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies

def get_movie_by_id(movie_id):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    

    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (movie_id,))
    
    movie = cursor.fetchone()
    cursor.close()
    conn.close()
    return movie

def add_movie(movie):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    

    try:
        cursor.execute(
            f"""INSERT INTO {TABLE_NAME} (title, year, genre, rating, description)
               VALUES (%s, %s, %s, %s, %s)""",
            (movie["title"], movie["year"], movie["genre"], movie["rating"], movie["description"])
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding movie: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_movie(movie_id):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    

    try:
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (movie_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting movie: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def update_movie(movie_id, movie):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    

    try:
        cursor.execute(
            f"""UPDATE {TABLE_NAME} SET title=%s, year=%s, genre=%s, rating=%s, description=%s 
               WHERE id=%s""",
            (movie["title"], movie["year"], movie["genre"], movie["rating"], movie["description"], movie_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating movie: {e}")
        return False
    finally:
        cursor.close()
        conn.close()