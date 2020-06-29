from .....config.oracle_connection import OracleConnection
from flask import request
from flask_restful import Resource
import os
import json


class rComponentG(Resource):
    def get(self, anio=0, mes=0, empresa=0, mercado=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteG.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        cpteG = []
        data = self.__execute_query()
        for result in data:
            cpteG.append(
                {
                    'ANO': result[19],
                    'MES': result[20],
                    'values': {
                        'DCR': [
                            result[22], # C16
                            result[0],  # C12
                            result[9],  # C13
                            result[1],  # C14
                            result[10], # C15
                        ],
                        'Qc': [
                            result[23], #C17
                        ],
                        'Pc': [
                            result[24], #C22
                            result[4],  #C1
                            result[2],  #C2
                            result[5],  #C3
                            result[6],  #C4
                            result[3],  #C5
                            result[11], #C6
                        ],
                        'Qb': [
                            result[25], #C18
                        ],
                        'Pb': [
                            result[26], #C23
                            result[7],  #C7
                            result[8],  #C8
                        ],
                        'Qagd': [
                            result[27], #C21
                            result[12], #C19
                            result[13], #20
                        ],
                        'McAplicado': [
                            result[28], #C11
                            result[21], #C9
                            result[18], #10
                        ],
                        'FAJ': [
                            result[14], #C24
                        ],
                        'ALFA': [
                            result[15], #C25
                        ],
                        'GTransitorio': [
                            result[16], #C26
                        ],
                        'GContratos': [
                            result[29], #C29
                        ],
                        'GBolsa': [
                            result[30], #C30
                        ],
                        'CFNC': [
                            result[17], #C27
                        ],
                        'CGeneracion': [
                            result[31]  #C28
                        ],
                    },
                }
            )
        return cpteG

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