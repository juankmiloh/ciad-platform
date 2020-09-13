from ....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import json


class gInfoADD(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()

    def get(self, mercado=0):
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        data = self.__execute_query()
        return data

    def __execute_query(self):
        print("GET MERCADO ---> ", self.__MERCADO_ARG)
        if self.__MERCADO_ARG == 0:
            # Consultar todos los registros
            result = []
            query = self.connection.infoADD.find()
            for item in query:
                # print(result)
                item['_id'] = str(item['_id'])
                result.append(item)
            return result
        else:
            # Consultar un registro especifico
            result = []
            objeto = {}
            mercado = 'm_' + str(self.__MERCADO_ARG)
            query = self.connection.infoADD.find({'key':0}, {'mercados.' + mercado: 1})
            lista = list(query)
            if len(lista) > 0:
                # print('lista > ', lista)
                if lista[0]['mercados']:
                    sizeArray = len(lista[0]['mercados'][mercado])
                    print("___________ SIZEARRAY _____________")
                    print(sizeArray)
                    objeto['mercado'] = mercado
                    for key, value in lista[0]['mercados'][mercado][sizeArray-1].items():
                        objeto[key] = value
                    result.append(objeto)
                    return result

    def post(self):
        req = request.args.get('params')
        print("POST MODEL ---> ", req)
        # Insertar datos
        self.connection.infoADD.insert_one(
            json.loads(req)
        )
        return req

    def put(self):
        req_model = request.args['params']
        req_mercado = 'm_' + str(request.args.get('mercado'))
        print('PUT MODEL ---> ', req_model)
        # Modificar datos
        self.connection.infoADD.update_one(
            {"key": 0},
            {"$push": {"mercados."+req_mercado: {"$each": [json.loads(req_model)]}}}
        )
        return req_model

    def delete(self):
        req_mercado = 'm_' + str(request.args.get('mercado'))
        # Borrar documento
        self.connection.infoADD.delete_one(
            {"key": 0},
            # {'mercados.' + mercado: 1}
        )
        return self.__KEY_ARG
