from ....config.oracle_connection import OracleConnection
from flask import request
from flask_restful import Resource
import os
import json


class rCostoUnitario(Resource):
    def get(self, anio=0, mes=0, empresa=0, mercado=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/costo_unitario.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        cu = []
        data = self.__execute_query()
        for result in data:
            cu.append(
                {
                    'id_empresa': result[12],
                    'id_mercado': result[1],
                    'ano': result[13],
                    'mes': result[14],
                    'nt_prop': result[4],
                    'GM': result[5],
                    'TM': result[6],
                    'PRNM': result[7],
                    'DNM': result[8],
                    'CVM': result[9],
                    'RM': result[10],
                    'CUVM': result[11]
                }
            )
        return cu

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________ ANIO ____________")
        print(self.__ANIO_ARG)
        print("____________________________")
        print("________ MES ____________")
        print(self.__PERIODO_ARG)
        print("____________________________")
        print("________ EMPRESA ____________")
        print(self.__EMPRESA_ARG)
        print("____________________________")
        print("________ MERCADO ____________")
        print(self.__MERCADO_ARG)
        print("____________________________")
        print("_________QUERY______________")
        print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        return cursor
