from ...config.oracle_connection import OracleConnection
from flask import request
from flask_restful import Resource
import os
import json


class CausasInterrupcion(Resource):
    def get(self, causa=0):
        self.__CAUSA_ARG = causa if causa != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/interrupciones/")
        file = "/causas.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        causas = []
        data = self.__execute_query()
        for result in data:
            causas.append(
                {
                    'cod_causa': result[0],
                    'col_sui': result[1],
                    'descripcion': result[2]
                }
            )
        return causas

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________CAUSA____________")
        print(self.__CAUSA_ARG)
        print("____________________________")
        print("_________QUERY______________")
        print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, CAUSA_ARG=self.__CAUSA_ARG)
        return cursor
