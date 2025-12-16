import mysql.connector
from movie_service.connection import get_connection

def create_user(user_data):
    """Inserts a new user into the users table."""
    connection = get_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (user_data['username'], user_data['email'], user_data['password']))
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_user_by_id(user_id):
    """Retrieves user data by their ID."""
    connection = get_connection()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    query = "SELECT id, username, email, created_at FROM users WHERE id = %s"
    try:
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_user(user_id):
    """Deletes a user record from the database."""
    connection = get_connection()
    if not connection:
        return False

    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id = %s"
    try:
        cursor.execute(query, (user_id,))
        connection.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()