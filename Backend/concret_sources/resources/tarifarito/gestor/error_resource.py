from ....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import json


class gD097Error(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()

    def get(self, f_inicial='', f_final=''):
        self.__FINICIAL_ARG = f_inicial if f_inicial != '' else ''
        self.__FFINAL_ARG = f_final if f_final != '' else ''
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
        print("___________ GET FINICIAL_____________")
        print(self.__FINICIAL_ARG)
        print("_________________________________")
        if self.__FINICIAL_ARG == '':
            # Consultar todos los registros
            mydoc = self.connection.infoD097Error.find()
        elif self.__FINICIAL_ARG != '' and self.__FFINAL_ARG == '':
            # Consultar un registro especifico por fecha inicial
            mydoc = self.connection.infoD097Error.find(
                {"f_inicial": self.__FINICIAL_ARG},
            )
        else:
            # Consultar un registro especifico por ambas fechas
            mydoc = self.connection.infoD097Error.find(
                {"f_inicial": self.__FINICIAL_ARG, "f_final": self.__FFINAL_ARG},
            )
        return mydoc

    def post(self):
        req = request.args.get('params')
        print("_________ POST MODEL _____________")
        print(req)
        print("_________________________________")
        # Insertar datos
        self.connection.infoD097Error.insert_one(
            json.loads(req)
        )
        return req

    def put(self, f_inicial='', f_final=''):
        self.__FINICIAL_ARG = f_inicial if f_inicial != '' else ''
        self.__FFINAL_ARG = f_final if f_final != '' else ''
        req_model = request.args['params']
        req_empresa = request.args.get('empresa')
        print("_________ PUT MODEL _____________")
        print(req_model)
        print("_________________________________")
        # Modificar datos
        self.connection.infoD097Error.update_one(
            {"f_inicial": self.__FINICIAL_ARG, "f_final": self.__FFINAL_ARG},
            {"$push": {"empresas."+req_empresa: {"$each": [json.loads(req_model)]}}}
        )
        return req_model

    def delete(self, f_inicial=''):
        self.__FINICIAL_ARG = f_inicial if f_inicial != '' else ''
        print("_________ DELETE FINICIAL ___________")
        print(self.__FINICIAL_ARG)
        print("_________________________________")
        # Borrar documento
        self.connection.infoD097Error.delete_one(
            {"f_inicial": self.__FINICIAL_ARG}
        )
        return self.__FINICIAL_ARG
