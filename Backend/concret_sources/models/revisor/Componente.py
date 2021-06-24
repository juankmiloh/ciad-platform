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
        self.connection = serviceConnection()

    # Se obtienen todos los valores registrados del componente para (1) empresa
    # Cuando el valor del mercado = 0 , se obtiene el componente para todos los mercados
    # Cuando el valor del mercado != 0 , se obtiene el componente para un mercado especifico
    def get_values_component_SUI(self):
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
        # print("------------------ QUERY -------------------------------")
        # print(self.__query)
        self.cursorSUI = self.connection.get_connectionSUI()
        print('-- CPTE -- ', self.__COMPONENTE)
        if self.__NTPROP_ARG == "No":
            if self.__COMPONENTE == 'DTUN':
                self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG)
            elif self.__COMPONENTE == 'R':
                self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, PERIODO_ARG_MENOS1=self.__PERIODO_ARG - 1, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
            elif self.__COMPONENTE == 'C':
                self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, PERIODO_ARG_MENOS1=self.__PERIODO_ARG - 1, PERIODO_ARG_MENOS2=self.__PERIODO_ARG - 2, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
            else:
                self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        else:
            if self.__COMPONENTE == 'T':
                self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG, NTPROP_ARG=self.__NTPROP_ARG)
        return self.cursorSUI
