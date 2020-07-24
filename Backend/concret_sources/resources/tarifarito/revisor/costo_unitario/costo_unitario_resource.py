from .....config.oracle_connection import OracleConnection
from .....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import os
import json
import pandas as pd


class rCostoUnitario(Resource):
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
        cpteP097 = []
        data = self.__execute_query()

        cpteG = self.__getData_cpteG(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG)
        cpteG = pd.DataFrame(cpteG)
        
        cpteT = self.__getData_cpteT(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG)
        cpteT = pd.DataFrame(cpteT)
        
        cpteP097 = self.__getData_cpteP097(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG)
        cpteP097 = pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5'])

        gestorP097 = self.__getVariables()

        cpteP097 = pd.merge(cpteP097, gestorP097, on='mercado')

        cpteP097['c15'] = 0

        cpteP097['c8'] = cpteP097['c2'] + cpteP097['c3'] + cpteP097['c4'] +cpteP097['c5'] +cpteP097['c6'] + cpteP097['c7'] 

        cpteP097['c9'] = (cpteP097['c3'] + cpteP097['c5'] + cpteP097['c7']) / cpteP097['c8']

        cpteP097['c16'] = cpteP097['c1'] * (cpteP097['c10'] / 100 + cpteP097['c9']) / (1 - (cpteP097['c10']/100 + cpteP097['c9']))

        cpteP097['c20'] = (cpteP097['c14']*cpteP097['c10']) / (1 - cpteP097['c10'] / 100 ) + cpteP097['c15']

        cpteP097['c17'] = (cpteP097['c1']*(cpteP097['c11']/100 + cpteP097['c9'])) / (1 - (cpteP097['c11'] / 100 + cpteP097['c9']))

        cpteP097['c21'] = (cpteP097['c14'] * cpteP097['c11']) / (1 - cpteP097['c11']/100) + cpteP097['c15']

        cpteP097['c18'] = (cpteP097['c1'] * (cpteP097['c12'] / 100 + cpteP097['c9']) ) / ( 1 - ( cpteP097['c12'] / 100 + cpteP097['c9']))

        cpteP097['c22'] = (cpteP097['c14'] * cpteP097['c12']) / (1 - cpteP097['c12']/100) + cpteP097['c15']

        cpteP097['c19'] = (cpteP097['c1'] * (cpteP097['c13'] / 100 + cpteP097['c9']) ) / ( 1 - ( cpteP097['c13'] / 100 + cpteP097['c9']))

        cpteP097['c23'] = (cpteP097['c14'] * cpteP097['c13']) / (1 - cpteP097['c13']/100) + cpteP097['c15']

        cpteP097['nt1'] =  cpteP097['c16'] +  cpteP097['c20']

        cpteP097['nt2'] =  cpteP097['c17'] +  cpteP097['c21']

        cpteP097['nt3'] =  cpteP097['c18'] +  cpteP097['c22']

        cpteP097['nt4'] =  cpteP097['c19'] +  cpteP097['c23']       

        for result in data:
            find = (cpteG[21] == result[12]) & (cpteG[22] == result[1]) & (cpteG[19] == result[13]) & (cpteG[20] == result[14])
            calculado_g = cpteG.loc[find][33].tolist()[0]
            find = (cpteT[0] == result[12]) & (cpteT[1] == result[1]) & (cpteT[3] == result[13]) & (cpteT[4] == result[14]) & (cpteT[2] == result[4])
            calculado_t = cpteT.loc[find][6].tolist()[0]
            # EMPRESA - MERCADO - ANIO - PERIODO
            find = (cpteP097['empresa'] == result[12]) & (cpteP097['mercado'] == result[1]) & (cpteP097['ano'] == result[13]) & (cpteP097['mes'] == result[14])

            print(cpteP097['nt1'])

            if result[4].find('1') != -1:
                calculado_p097_nt = cpteP097['nt1'].tolist()[0]
            if result[4].find('2') != -1:
                calculado_p097_nt = cpteP097['nt2'].tolist()[0]
            if result[4].find('3') != -1:
                calculado_p097_nt = cpteP097['nt3'].tolist()[0]
            if result[4].find('4') != -1:
                calculado_p097_nt = cpteP097['nt4'].tolist()[0]

            print(calculado_p097_nt)

            modelG = [{ 'value': "g", 'cpte_publicado': result[5], 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
            modelT = [{ 'value': "t", 'cpte_publicado': result[6], 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
            modelP097 = [{ 'value': "p", 'cpte_publicado': result[7], 'cpte_calculado': calculado_p097_nt, 'label_publicado': 'Componente P097 publicado:', 'label_calculado': 'Componente P097 calculado:' }]
            componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP097}]
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
    
    # --------------------------------------
    # Calculo componente P
    # --------------------------------------
    def __getData_cpteP097(self, ano, mes, empresa, mercado):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteP097.json"
        source = json.load(open(path + file))
        query = ''.join(source["query"])

        data = self.__execute_query_cpteP(query, ano, mes, empresa, mercado)
        return data

    def __execute_query_cpteP(self, query, ano, mes, empresa, mercado):
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
        # print("SQL:", query)
        print("____________________________")
        cursor.execute(query, ANIO_ARG=ano, PERIODO_ARG=mes, EMPRESA_ARG=empresa, MERCADO_ARG=mercado)
        return cursor

    def __getVariables(self):
        result = list(self.connection.perdidasSTN.find({"anio": 0}))
        key_mercados = []
        for x in result:
            for key, value in x['mercados'].items():
                key_mercados.append(key)

        obj = []

        for m in key_mercados:
            mercado = result[0]['mercados'][m]
            no_mercado = int(m.split('_')[1])
            pr1 = mercado[len(mercado)-1]['pr1']
            pr2 = mercado[len(mercado)-1]['pr2']
            pr3 = mercado[len(mercado)-1]['pr3']
            pr4 = mercado[len(mercado)-1]['pr4']
            obj.append([no_mercado,pr1,pr2,pr3,pr4])

        df = pd.DataFrame(obj,columns=['mercado','c10','c11','c12','c13'])
        return df