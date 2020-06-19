from ...config.oracle_connection import OracleConnection
from flask import request
from flask_restful import Resource
import os
import json


class AniosInterrupcion(Resource):
    def get(self, anio=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/interrupciones/")
        file = "/anios.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        anios = []
        if self.__ANIO_ARG != 0:  # se ejecuta cuando se envia el año
            print("________Se recibe año________________")
            print(self.__ANIO_ARG)
            print("____________________________")
            data = self.__execute_query()
            for pqr in data:
                anios.append(
                    {
                        'anio': pqr[0],
                        'mes': pqr[1]
                    }
                )
            return anios
        else:  # se ejecuta cuando se quieren obtener todos los años
            print("________No se recibe año________________")
            print(self.__ANIO_ARG)
            print("____________________________")
            data = self.__execute_query()
            anio = 0
            for pqr in data:
                if anio != pqr[0]:
                    anios.append(
                        {
                            'anio': pqr[0]
                        }
                    )
                anio = pqr[0]
            return anios

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________ANIO________________")
        print(self.__ANIO_ARG)
        print("____________________________")
        print("_________QUERY______________")
        print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG)
        return cursor
