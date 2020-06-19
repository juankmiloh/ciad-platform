import datetime
import csv
import os
import json

from flask import send_from_directory
from flask import send_file  # descargar archivos

from flask import request
from flask_restful import Resource
from ...config.oracle_connection import OracleConnection


class EmpresasRsource(Resource):
    def get(self, servicio=""):

        self.__SERVICIO_ARG = servicio if servicio != "" else "TODOS"
        self.__SERVICIO_ARG = self.__SERVICIO_ARG.upper()

        self.__upload_source()

        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/pqrs/")
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

        for pqr in data:
            empresas.append(
                {
                    'cod_empresa': pqr[0],
                    'nombre': pqr[1],
                    'servicio': pqr[2],
                }
            )

        return empresas

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()

        print("____________________________")
        print(self.__SERVICIO_ARG)
        print("____________________________")

        print("____________________________")
        print("SQL:", self.__query)
        print("____________________________")

        cursor.execute(self.__query, SERVICIO_ARG=self.__SERVICIO_ARG)

        return cursor
