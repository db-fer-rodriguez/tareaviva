from pymongo import MongoClient

class Archivo:
    def __init__(self, tarea_id, nombre_archivo, tipo_archivo, ruta_archivo):
        self.tarea_id = tarea_id
        self.nombre_archivo = nombre_archivo
        self.tipo_archivo = tipo_archivo
        self.ruta_archivo = ruta_archivo

    def to_dict(self):
        return {
            "tarea_id": self.tarea_id,
            "nombre_archivo": self.nombre_archivo,
            "tipo_archivo": self.tipo_archivo,
            "ruta_archivo": self.ruta_archivo
        }

    @staticmethod
    def from_dict(data):
        return Archivo(
            data["tarea_id"],
            data["nombre_archivo"],
            data["tipo_archivo"],
            data["ruta_archivo"]
        )