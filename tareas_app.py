import os
import mysql.connector
from dotenv import load_dotenv
from pymongo import MongoClient
from mongo_models import Archivo  # Asegúrate de tener este archivo y la clase Archivo

load_dotenv()

# Funciones de conexión (simplificadas)
def get_mysql_connection():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT"))
        )
    except mysql.connector.Error as e:
        print(f"Error MySQL: {e}")
        return None

def get_mongo_client():
    """Establece y devuelve un cliente de conexión a MongoDB Atlas."""
    try:
        return MongoClient(os.getenv("MONGODB_URI"))
    except Exception as e:
        print(f"Error MongoDB: {e}")
        return None

# Funciones de manipulación (simplificadas)
def crear_tarea(titulo, descripcion, archivos=None):
    """Crea una nueva tarea en MySQL y agrega archivos a MongoDB (opcional)."""
    try:
        with get_mysql_connection() as conn, conn.cursor() as cursor:
            cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)", (titulo, descripcion))
            conn.commit()
            tarea_id = cursor.lastrowid
            if archivos:
                for archivo in archivos:
                    agregar_archivo(tarea_id, archivo["nombre"], archivo["tipo"], archivo["ruta"])
            print(f"Tarea '{titulo}' creada.")
    except Exception as e:
        print(f"Error: {e}")

def consultar_tareas():
    """Consulta y muestra todas las tareas de MySQL y sus archivos adjuntos de MongoDB."""
    try:
        with get_mysql_connection() as conn, conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tareas")
            for tarea in cursor.fetchall():
                print(f"ID: {tarea[0]}, Título: {tarea[1]}, Descripción: {tarea[2]}")
                consultar_archivos(tarea[0])
    except Exception as e:
        print(f"Error: {e}")

def borrar_tarea(tarea_id):
    """Borra una tarea de MySQL y sus archivos adjuntos de MongoDB."""
    try:
        with get_mysql_connection() as conn, conn.cursor() as cursor:
            cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
            conn.commit()
            borrar_archivos(tarea_id)
            print(f"Tarea {tarea_id} borrada.")
    except Exception as e:
        print(f"Error: {e}")

def agregar_archivo(tarea_id, nombre, tipo, ruta):
    """Agrega un archivo a MongoDB para una tarea específica."""
    try:
        client = get_mongo_client()
        db = client.tareaviva_db
        db.archivos.insert_one(Archivo(tarea_id, nombre, tipo, ruta).to_dict())
        client.close()
        print(f"Archivo '{nombre}' agregado.")
    except Exception as e:
        print(f"Error: {e}")

def consultar_archivos(tarea_id):
    """Consulta y muestra los archivos adjuntos de MongoDB para una tarea específica."""
    try:
        client = get_mongo_client()
        archivos = client.tareaviva_db.archivos.find({"tarea_id": tarea_id})
        for archivo in archivos:
            a = Archivo.from_dict(archivo)
            print(f"  - {a.nombre_archivo} ({a.tipo_archivo}): {a.ruta_archivo}")  # Corrección aquí
        client.close()
    except Exception as e:
        print(f"Error: {e}")

def borrar_archivos(tarea_id):
    """Borra todos los archivos adjuntos de MongoDB para una tarea específica."""
    try:
        client = get_mongo_client()
        client.tareaviva_db.archivos.delete_many({"tarea_id": tarea_id})
        client.close()
        print(f"Archivos de tarea {tarea_id} borrados.")
    except Exception as e:
        print(f"Error: {e}")

# Interfaz de usuario (simplificada)
while True:
    print("\n1. Crear | 2. Consultar | 3. Borrar | 4. Salir")
    opcion = input("Opción: ")

    if opcion == "1":
        titulo = input("Título: ")
        descripcion = input("Descripción: ")
        archivos = []
        while True:
            ruta = input("Archivo (o Enter): ")
            if not ruta:
                break
            archivos.append({"nombre": os.path.basename(ruta), "tipo": os.path.splitext(ruta)[1][1:], "ruta": ruta})
        crear_tarea(titulo, descripcion, archivos)

    elif opcion == "2":
        consultar_tareas()

    elif opcion == "3":
        borrar_tarea(int(input("ID tarea: ")))

    elif opcion == "4":
        break

    else:
        print("Opción inválida.")