import json
from pymongo import MongoClient

# -- CLASE QUE GESTIONA LA CONEXION CON LA BASE DE DATOS MONGODB
class MongoConnection():
    def __init__(self):
        credentials = json.load(open("config/configuration.json"))
        client = MongoClient(
            credentials["mongo_credentials"]["host"], 
            credentials["mongo_credentials"]["port"]
        )
        self.db = client[credentials["mongo_credentials"]["db"]]
        self.collection = self.db["incidencias_empresa_xm"]
        print(" -- MONGODB CONNECTION SUCCESFULL !!")

    def get_connection(self):
        return self.db

