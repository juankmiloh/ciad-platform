from .....config.oracle_connection import OracleConnection
from .....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import os
import json


class rComponentT(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()

    def get(self, anio=0, mes=0, empresa=0, mercado=0, ntprop=""):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__NTPROP_ARG = ntprop if ntprop != "" else "TODOS"
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteT.json"
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
                    'ano': result[3],
                    'mes': result[4],
                    'empresa': result[0],
                    'mercado': result[1],
                    'ntprop': result[2],
                    'values': {
                        'DATAPUBLICADA': [
                            result[5], #C3 - STNAGENTE
                            result[6]  #C4 - STNLAC
                        ],
                        'CALCULOSSPD': [
                            0, #C - TLAC
                            0, #C - DTLAC
                            0  #C - CPT
                        ],
                        'DIFERENCIA': [
                            0, #C - CPTAGENTE
                            0  #C - CPTLAC
                        ]
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
        # print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG, NTPROP_ARG=self.__NTPROP_ARG)
        return cursor

    def post(self):
        req = request.args.get('params')
        print("_________ POST MODEL _____________")
        # print(req)
        print("_________________________________")
        # Insertar datos
        self.connection.componentT.insert_one(
            json.loads(req)
        )
        return req
