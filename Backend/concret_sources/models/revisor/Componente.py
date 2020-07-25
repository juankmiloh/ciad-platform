from ...util.ServiceConnection import serviceConnection
import os
import json
import pandas as pd


class Componente():

    def __init__(self, componente, ano, mes, empresa, mercado, ntprop):
        self.__COMPONENTE = componente
        self.__ANIO_ARG = ano
        self.__PERIODO_ARG = mes
        self.__EMPRESA_ARG = empresa
        self.__MERCADO_ARG = mercado
        self.__NTPROP_ARG = ntprop
        connection = serviceConnection()
        self.cursorSUI = connection.get_connectionSUI()
        self.connMDB = connection.get_connectionMDB()

    def get_component_cu(self):
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpte" + self.__COMPONENTE + ".json"
        source = json.load(open(path + file))
        self.__query = ''.join(source["query"])
    
    def __getData(self):
        data = self.__execute_query_cpte()
        return data

    def __execute_query_cpte(self):
        if self.__NTPROP_ARG == "No":
            self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        else:
            self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG, NTPROP_ARG=self.__NTPROP_ARG)
        return self.cursorSUI

    def merge_perdidas_P097(self, dataFrame):
        cpteP097 = dataFrame

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

        return cpteP097

    def __getVariables(self):
        result = list(self.connMDB.perdidasSTN.find({"anio": 0}))
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