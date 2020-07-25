from ..util.ServiceConnection import serviceConnection
from tools import Tools
import os
import json


class MercadosModel():

    def __init__(self, mercado):
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        connection = serviceConnection()
        self.cursor = connection.get_connectionSUI()

    def getMercados(self):
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/mercados.json"
        source = json.load(open(path + file))
        self.__query = ''.join(source["query"])

    def __getData(self):
        mercados = []
        data = self.__execute_query()
        for result in data:
            mercados.append({
                'id_mercado': result[0],
                'nom_mercado': result[1],
                'estado': result[2]
            })
        return mercados

    def __execute_query(self):
        self.cursor.execute(self.__query, MERCADO_ARG=0)
        return self.cursor
