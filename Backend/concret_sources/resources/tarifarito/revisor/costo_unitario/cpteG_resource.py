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
                            round(result[22], 3), # C16
                            round(result[0], 3), # C12
                            round(result[9], 3), # C13
                            round(result[1], 3), # C14
                            round(result[10], 3) # C15
                        ],
                        'Qc': [
                            round(result[23], 3) #C17
                        ],
                        'Pc': [
                            round(result[24], 3), #C22
                            round(result[4], 3), #C1
                            round(result[2], 3), #C2
                            round(result[5], 3), #C3
                            round(result[6], 3), #C4
                            round(result[3], 3), #C5
                            round(result[11], 3) #C6
                        ],
                        'Qb': [
                            round(result[25], 3) #C18
                        ],
                        'Pb': [
                            round(result[26], 3), #C23
                            round(result[7], 3), #C7
                            round(result[8], 3) #C8
                        ],
                        'Qagd': [
                            round(result[27], 3), #C21
                            round(result[12], 3), #C19
                            round(result[13], 3) #20
                        ],
                        'McAplicado': [
                            round(result[28], 3), #C11
                            round(result[21], 3), #C9
                            round(result[18], 3) #10
                        ],
                        'FAJ': [
                            round(result[14], 3) #C24
                        ],
                        'ALFA': [
                            round(result[15], 3) #C25
                        ],
                        'GTransitorio': [
                            round(result[16], 3) #C26
                        ],
                        'GContratos': [
                            round(result[29], 3) #C29
                        ],
                        'GBolsa': [
                            round(result[30], 3) #C30
                        ],
                        'CFNC': [
                            round(result[17], 3) #C27
                        ],
                        'CGeneracion': [
                            round(result[31], 3)  #C28
                        ]
                    }
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
