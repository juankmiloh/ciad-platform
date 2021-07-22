from ...config.oracle_connection import OracleConnection
from flask import request
from flask_restful import Resource
import os
import json


class empresasTarifarito(Resource):
    def get(self, empresa=0):
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/empresas.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        empresas = []
        data = self.__execute_query()
        for result in data:
            if result[0] == 20217:
                lst = list(result)
                lst[1] = "UNIDAD DE SERVICIOS PUBLICOS - VAUPES"
                result = tuple(lst)
            elif result[0] == 497:
                lst = list(result)
                lst[1] = "PROMOTORA DE ENERGIA ELECTRICA DE CARTAGENA"
                result = tuple(lst)
            elif result[0] == 2452:
                lst = list(result)
                lst[1] = "COMERCIALIZADORA ANDINA DE ENERGIA"
                result = tuple(lst)
            elif result[0] == 1900:
                lst = list(result)
                lst[1] = "E.A.T. DE PRESTACION DE SERVCIOS PUBLICOS MOSQUERA"
                result = tuple(lst)
            elif result[0] == 3111:
                lst = list(result)
                lst[1] = "ENERGETICOS S.A.S. DISTRIBUIDORA"
                result = tuple(lst)
            elif result[0] == 1720:
                lst = list(result)
                lst[1] = "SOCIEDAD PRODUCTORA DE ENERGÍA DE SAN ANDRES Y PROV"
                result = tuple(lst)
            elif result[0] == 2261:
                lst = list(result)
                lst[1] = "TERMOCANDELARIA SOCIEDAD EN COMANDITA POR ACCIONES"
                result = tuple(lst)
            empresas.append(
                {
                    'cod_empresa': result[0],
                    'nombre': result[1],
                    'servicio': result[2],
                    'sigla': result[3],
                    'NIT': result[4]
                }
            )
        return empresas

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________EMPRESA____________")
        print(self.__EMPRESA_ARG)
        print("____________________________")
        # print("_________QUERY______________")
        # print("SQL:", self.__query)
        # print("____________________________")
        cursor.execute(self.__query, EMPRESA_ARG=self.__EMPRESA_ARG)
        return cursor
