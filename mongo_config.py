import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

def get_mongo_client():
    try:
        client = MongoClient(MONGODB_URI)
        print("Conexión a MongoDB Atlas exitosa!")
        return client
    except Exception as e:
        print(f"Error al conectar a MongoDB Atlas: {e}")
        return None

def close_mongo_client(client):
    if client:
        client.close()