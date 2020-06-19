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
                    # FT10
                    'C12_C4': result[0],
                    'C14_C6': result[1],
                    'C2_C2': result[2],
                    'C5_C3': result[3],
                    # FT9
                    'C1_C7': result[4],
                    'C3_C2': result[5],
                    'C4_C8': result[6],
                    'C7_C5': result[7],
                    'C8_C6': result[8],
                    'C13_C15': result[9],
                    'C15_C16': result[10],
                    'C6_C3': result[11],
                    'C19_C9': result[12],
                    'C20_C10': result[13],
                    'C24_C13': result[14],
                    'C25_C14': result[15],
                    'C26_C11': result[16],
                    'C27_C12': result[17],
                    'C10_C4': result[18],
                    # FT13
                    'C9_C1': result[21],
                    # CALCULOS FINALES
                    'C16_DCR': result[22],
                    'C17_QC': result[23],
                    'C22_PC': result[24],
                    'C18_QB': result[25],
                    'C23_PB': result[26],
                    'C21_QAGD': result[27],
                    'C11_MCAPLICADO': result[28],
                    'C29_GCONTRATOS': result[29],
                    'C30_GBOLSA': result[30],
                    'C28_CG': result[31]
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
