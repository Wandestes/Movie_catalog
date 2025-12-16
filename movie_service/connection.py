import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Creates and returns a connection to the MySQL database.
    Used by both movie_service and user_service.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="24062006_Oleya",  # Your specific password
            database="movie_catalog",
            port=3306
        )
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Successfully connected to movie_catalog database!")
        conn.close()