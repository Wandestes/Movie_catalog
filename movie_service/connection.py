# movie_service/connection.py
import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="movie_catalog",
            port=3306
        )
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL connection error: {err}") # ЦЕ ВАШ PRINT!
        return None # ПОВЕРНЕННЯ None ВАЖЛИВЕ