import os
from pymongo import MongoClient
import json

PATH = os.path.dirname(os.path.realpath(__file__))

# -- CLASE QUE GESTIONA LA CONEXION CON LA BASE DE DATOS MONGODB
class MongoConnection():
    def __init__(self):
        credentials = json.load(open(PATH + "/configuration.json"))
        client = MongoClient(
            credentials["mongo_credentials"]["host"], 
            credentials["mongo_credentials"]["port"]
        )
        self.db = client[credentials["mongo_credentials"]["db"]]
        # self.collection = self.db["incidencias_empresa_xm"]
        print(" -- MONGODB CONNECTION SUCCESFULL !!")

    def get_connection(self):
        return self.db

# mongodbConnection = MongoConnection()
# connection = mongodbConnection.get_connection()
# mydoc = connection.nivelTolerancia.find() # Obtener todos los documentos de la coleccion
# # mydoc = connection.nivelTolerancia.find({"nivelT": 1}) # Obtener un documento especifico de la coleccion
# for x in mydoc:
#     print(x)
# connection.usuarios.drop() # Eliminar coleccion
# connection.usuarios.insert_one({"name": "Juan", "apellido": "Herrera"}) # Insertar datos
# connection.usuarios.insert_one({"name": "Diana", "apellido": "nn"}) # Insertar datos
# connection.usuarios.insert_one({"name": "Ana Maria", "apellido": "Herrera"}) # Insertar datos
# connection.usuarios.update_one({"name": "Diana"}, {"$set": {"apellido": "Moreno"}}) # Actualizar un solo documento especifico
# connection.usuarios.update_many({"name": "Diana"}, {"$set": {"apellido": "Moreno"}}) # Actualizar todos los documentos con un campo igual
# # connection.usuarios.delete_one({"apellido": "Moreno"}) # Borrar un documento especifico
# # connection.usuarios.delete_many({"apellido": "Moreno"}) # Borrar todos los documentos con un campo igual
# # connection.usuarios.delete_one({'name': 'Juan'}) # Eliminar documento especifico

