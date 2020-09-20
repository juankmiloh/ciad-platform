from ...util.ServiceConnection import serviceConnection
import math
import os
import json
from concret_sources.models.revisor.formulas.FormulaTarifas import FormulaTarifas


class Tarifas():

    # Se inicializan las variables de la clase (recibidas desde el ENDPOINT)
    def __init__(self, anio, mes, empresa, mercado, ntprop):
        self.__ANIO_ARG = anio
        self.__PERIODO_ARG = mes
        self.__EMPRESA_ARG = empresa
        self.__MERCADO_ARG = mercado
        self.__NTPROP_ARG = ntprop
        self.connection = serviceConnection()

    # Se obtienen los valores publicados por la empresa en FT3 - FT4
    def getTarifas(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/tarifas.json"
        source = json.load(open(path + file))
        self.__query = ''.join(source["query"])
        return self.getData()

    def getData(self):
        data = self.execute_query()
        return data

    def execute_query(self):
        self.cursor = self.connection.get_connectionSUI()
        self.cursor.execute(
            self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, 
            PERIODO_ARG_MENOS1=self.__PERIODO_ARG - 1, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG
        )
        return self.cursor

    # Función para calcular tarifas
    def get_values_tarifas(self, dataframe, ano, periodo):
        # print('RESULT > ', result[1])
        # print('dataframe > ', dataframe[1])
        # find = (dataframe[1] == result[1]) & (dataframe[4] == result[4])
        tarifas = FormulaTarifas().calcular_tarifas(dataframe, ano, periodo)
        return tarifas