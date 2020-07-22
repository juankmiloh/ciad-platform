from .....config.oracle_connection import OracleConnection
from flask import request
from flask_restful import Resource
import os
import json
import pandas as pd


class rCostoUnitario(Resource):
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
        file = "/costo_unitario.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        cu = []
        componentes = []
        cpteG = []
        cpteT = []
        data = self.__execute_query()

        cpteG = self.__getData_cpteG(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG)
        cpteG = pd.DataFrame(cpteG)
        
        cpteT = self.__getData_cpteT(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG)
        cpteT = pd.DataFrame(cpteT)

        for result in data:
            find = (cpteG[21] == result[12]) & (cpteG[22] == result[1]) & (cpteG[19] == result[13]) & (cpteG[20] == result[14])
            calculado_g = cpteG.loc[find][33].tolist()[0]
            find = (cpteT[0] == result[12]) & (cpteT[1] == result[1]) & (cpteT[3] == result[13]) & (cpteT[4] == result[14]) & (cpteT[2] == result[4])
            calculado_t = cpteT.loc[find][6].tolist()[0]
            modelG = [{ 'value': "g", 'cpte_publicado': result[5], 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
            modelT = [{ 'value': "t", 'cpte_publicado': result[6], 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
            componentes = [{'component_g': modelG, 'component_t': modelT}]
            cu.append(
                {
                    'id_empresa': result[12],
                    'id_mercado': result[1],
                    'mercado': result[18],
                    'ano': result[13],
                    'mes': result[14],
                    'nt_prop': result[4],
                    'componentes': componentes,
                    # 'GM': result[5],
                    # 'TM': result[6],
                    # 'PRNM': result[7],
                    # 'DNM': result[8],
                    # 'CVM': result[9],
                    # 'RM': result[10],
                    # 'CUVM': result[11]
                }
            )
            componentes = []
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
    def __getData_cpteG(self, ano, mes, empresa, mercado):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteG.json"
        source = json.load(open(path + file))
        query = ''.join(source["query"])

        cpteG = []
        data = self.__execute_query_cpteG(query, ano, mes, empresa, mercado)
        return data

    def __execute_query_cpteG(self, query, ano, mes, empresa, mercado):
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

    # --------------------------------------
    # Calculo componente T
    # --------------------------------------
    def __getData_cpteT(self, ano, mes, empresa, mercado):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteT.json"
        source = json.load(open(path + file))
        query = ''.join(source["query"])

        data = self.__execute_query_cpteT(query, ano, mes, empresa, mercado)
        return data

    def __execute_query_cpteT(self, query, ano, mes, empresa, mercado):
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
        print("_________ QUERY COMPONENTE T ______________")
        print("SQL:", query)
        print("____________________________")
        cursor.execute(query, ANIO_ARG=ano, PERIODO_ARG=mes, EMPRESA_ARG=empresa, MERCADO_ARG=mercado, NTPROP_ARG=self.__NTPROP_ARG)
        return cursor