"""Módulo que contiene funciones para establecer y cerrar una conexión a una base de datos MySQL."""

import mysql.connector
from dotenv import load_dotenv
import os  # Para obtener variables de entorno

load_dotenv()

def get_mysql_connection():
    """
    Establece una conexión a la base de datos MySQL.

    Retorna:
        Una conexión a la base de datos MySQL si la conexión es exitosa, o None si hay un error.
    """
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
            port=port
        )

        # Seleccionar la base de datos con USE (alternativa)
        if database:
            cursor = connection.cursor()
            cursor.execute(f"USE {database}")
            cursor.close()
            print(f"Base de datos '{database}' seleccionada correctamente.")  # Mensaje de éxito
        else:
            print("Advertencia: No se especificó ninguna base de datos en las variables de entorno.")

        return connection
    except mysql.connector.Error as error:
        print("Error al conectar a MySQL:", error)
        return None

def close_mysql_connection(connection):
    if connection:
        connection.close()