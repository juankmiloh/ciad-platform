from ....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import json


class gIDaneTarifarito(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()

    def get(self, anio=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        return self.__getData()

    def __getData(self):
        anios = []
        data = self.__execute_query()
        for result in data:
            # print(result)
            result['_id'] = str(result['_id'])
            anios.append(result)
        return anios

    def __execute_query(self):
        print("___________ GET ANIO_____________")
        print(self.__ANIO_ARG)
        print("_________________________________")
        if self.__ANIO_ARG == 0:
            # Consultar todos los registros
            mydoc = self.connection.indicesDANE.find()
        else:
            # Consultar un registro especifico
            mydoc = self.connection.indicesDANE.find(
                {"anio": self.__ANIO_ARG}
            )
        return mydoc

    def post(self):
        req = request.args.get('params')
        print("_________ POST MODEL _____________")
        print(req)
        print("_________________________________")
        # Insertar datos
        self.connection.indicesDANE.insert_one(
            json.loads(req)
        )
        return req

    def put(self, anio=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        req_model = request.args['params']
        req_mes = request.args.get('mes')
        print("_________ PUT MODEL _____________")
        print(req_model)
        print("_________________________________")
        # Modificar datos
        self.connection.indicesDANE.update_one(
            {"anio": self.__ANIO_ARG},
            {"$push": {"meses."+req_mes: {"$each": [json.loads(req_model)]}}}
        )
        return req_model

    def delete(self, anio=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        print("_________ DELETE ANIO ___________")
        print(self.__ANIO_ARG)
        print("_________________________________")
        # Borrar documento
        self.connection.indicesDANE.delete_one(
            {"anio": self.__ANIO_ARG}
        )
        return self.__ANIO_ARG
