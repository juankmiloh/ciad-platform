from ...util.ServiceConnection import serviceConnection
import os
import json


class CostoUnitario():

    def __init__(self, anio, mes, empresa, mercado, ntprop):
        self.__ANIO_ARG = anio
        self.__PERIODO_ARG = mes
        self.__EMPRESA_ARG = empresa
        self.__MERCADO_ARG = mercado
        self.__NTPROP_ARG = ntprop
        connection = serviceConnection()
        self.cursor = connection.get_connectionSUI()

    def getCostoUnitario(self):
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/costo_unitario.json"
        source = json.load(open(path + file))
        self.__query = ''.join(source["query"])

    def __getData(self):
        data = self.__execute_query()
        return data

    def __execute_query(self):
        self.cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        return self.cursor
