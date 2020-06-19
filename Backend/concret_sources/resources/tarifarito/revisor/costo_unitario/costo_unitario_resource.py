from .....config.oracle_connection import OracleConnection
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
        cpteG = []
        data = self.__execute_query()
        id_mercado_inicial = 0
        id_mercado_temp = 0
        for result in data:
            id_mercado_inicial = result[1]
            if id_mercado_inicial != id_mercado_temp:
                cpteG = self.__getData_cpteG(result[13], result[14], result[12], result[1], result[5])
            cu.append(
                {
                    'id_empresa': result[12],
                    'id_mercado': result[1],
                    'mercado': result[1],
                    'ano': result[13],
                    'mes': result[14],
                    'nt_prop': result[4],
                    'component_g': cpteG
                    # 'GM': result[5],
                    # 'TM': result[6],
                    # 'PRNM': result[7],
                    # 'DNM': result[8],
                    # 'CVM': result[9],
                    # 'RM': result[10],
                    # 'CUVM': result[11]
                }
            )
            id_mercado_temp = id_mercado_inicial
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
        print("_________ QUERY CU ______________")
        # print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        return cursor

    # --------------------------------------
    # Calculo componente G
    # --------------------------------------
    def __getData_cpteG(self, ano, mes, empresa, mercado, cpte_publicado):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteG.json"
        source = json.load(open(path + file))
        # query que se quiere hacer y se concatena porque es un string
        query = ''.join(source["query"])

        cpteG = []
        data = self.__execute_query_cpteG(query, ano, mes, empresa, mercado)
        for result in data:
            cpteG.append(
                {
                    'value': "g",
                    'cpte_publicado': cpte_publicado,
                    'cpte_calculado': result[31],
                    'cpte_diferencia': cpte_publicado - result[31]
                }
            )
        return cpteG

    def __execute_query_cpteG(self, query, ano, mes, empresa, mercado,):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________ ANIO ____________")
        print(ano)
        print("____________________________")
        print("________ MES ____________")
        print(mes)
        print("____________________________")
        print("________ EMPRESA ____________")
        print(empresa)
        print("____________________________")
        print("________ MERCADO ____________")
        print(mercado)
        print("____________________________")
        print("_________ QUERY COMPONENTE G ______________")
        # print("SQL:", query)
        print("____________________________")
        cursor.execute(query, ANIO_ARG=ano, PERIODO_ARG=mes, EMPRESA_ARG=empresa, MERCADO_ARG=mercado)
        return cursor
