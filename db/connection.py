# db/connection.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="24062006_Oleya", # your password
            database="movie_catalog"
        )
        return connection
    except Error as e:
        print("MySQL connection error:", e)
        return None

