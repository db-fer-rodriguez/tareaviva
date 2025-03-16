import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_mysql_connection():
    try:
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")
        port = int(os.getenv("MYSQL_PORT"))

        print(f"Host: {host}, User: {user}, Password: {password}, Database: {database}, Port: {port}")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        return connection
    except mysql.connector.Error as error:
        print("Error al conectar a MySQL:", error)
        return None

def close_mysql_connection(connection):
    if connection:
        connection.close()