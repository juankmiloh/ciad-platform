from ...config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource


class usersTarifarito(Resource):
    def get(self, user=0):
        self.__USER_ARG = user if user != 0 else 0
        return self.__getData()

    def __getData(self):
        users = []
        data = self.__execute_query()
        for result in data:
            # print(result)
            result['_id'] = str(result['_id'])
            users.append(result)
        return users

    def __execute_query(self):
        mongodb_connection = MongoConnection()
        connection = mongodb_connection.get_connection()
        # connection.usuarios.drop() # Eliminar coleccion
        # connection.usuarios.insert_one({"name": "Diana", "apellido": "Moreno"}) # Insertar datos
        # connection.usuarios.insert_one({"name": "Ana Maria", "apellido": "Herrera"}) # Insertar datos
        # connection.usuarios.insert_one({"name": "Juan", "apellido": "Herrera", "nit": 1016040458}) # Insertar datos
        if self.__USER_ARG == 0:
            mydoc = connection.usuarios.find()
        else:
            mydoc = connection.usuarios.find({"nit": self.__USER_ARG})

        print("________USER________________")
        print(self.__USER_ARG)
        print("____________________________")
        return mydoc
    
    def post(self, user=0):
        return "ENTRO AL TARIFARITO POST!"
    
    def put(self, user=0):
        return "ENTRO AL PUT!"
    
    def delete(self, user=0):
        return "ENTRO AL DELETE!"
