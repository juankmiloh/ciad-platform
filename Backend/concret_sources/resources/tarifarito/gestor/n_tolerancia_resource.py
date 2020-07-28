from ....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import json


class gNToleranciaTarifarito(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def get(self, anio=0, mes=""):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__MES_ARG = mes if mes != "" else "TODOS"
        return self.__getData()

    def __getData(self):
        data = self.__execute_query()
        return data

    def __execute_query(self):
        # print("GET ANIO -> ", self.__ANIO_ARG)
        # print("GET MES -> ", self.__MES_ARG)
        mydoc = []
        if self.__ANIO_ARG == 0 and self.__MES_ARG == "TODOS":
            # Consultar todos los registros
            query = self.connection.nivelTolerancia.find()
            for result in query:
                # print(result)
                result['_id'] = str(result['_id'])
                mydoc.append(result)
        elif self.__ANIO_ARG != 0 and self.__MES_ARG == "TODOS":
            # Consultar un registro especifico por anio
            query = self.connection.nivelTolerancia.find(
                {"anio": self.__ANIO_ARG}
            )
            for result in query:
                # print(result)
                result['_id'] = str(result['_id'])
                mydoc.append(result)
        elif self.__ANIO_ARG != 0 and self.__MES_ARG != "TODOS":
            mes = self.meses[int(self.__MES_ARG) - 1]
            # Consultar un registro especifico por anio y mes
            objeto = {}
            lista = list(self.connection.nivelTolerancia.find({'anio': self.__ANIO_ARG}, {'meses.'+ mes +'': 1}))
            sizeArray = len(lista[0]['meses'][mes])
            # print("*SIZEARRAY -> ",  sizeArray)
            for key, value in lista[0]['meses'][mes][sizeArray-1].items():
                objeto[key] = value
            mydoc.append(objeto)
        return mydoc

    def post(self):
        req = request.args.get('params')
        print("_________ POST MODEL _____________")
        print(req)
        print("_________________________________")
        # Insertar datos
        self.connection.nivelTolerancia.insert_one(
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
        self.connection.nivelTolerancia.update_one(
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
        self.connection.nivelTolerancia.delete_one(
            {"anio": self.__ANIO_ARG}
        )
        return self.__ANIO_ARG
