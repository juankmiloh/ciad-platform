from ...util.ServiceConnection import serviceConnection
from flask import request
from flask_restful import Resource
import os
import json


class empresaMercadoTarifarito(Resource):
    def __init__(self):
        connection = serviceConnection()
        self.cursor = connection.get_connectionSUI()

    def get(self, empresa=0, mercado=0):
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/empresa_mercado.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        empresa = []
        data = self.__execute_query()
        if self.__EMPRESA_ARG != 0:
            for result in data:
                print("RESULT -> ", result[3])
                if result[3] != 0:
                    empresa.append(
                        {
                            'cod_empresa': result[0],
                            'nom_empresa': result[1],
                            'servicio': result[2],
                            'mercados': [{'cod_mercado': result[3], 'nom_mercado': result[4]}],
                        }
                    )
                else:
                    mercados = []
                    # print("TODOS LOS MERCADOS!")
                    # print(self.getMercados())
                    dataMercados = self.getMercados()
                    for mercado in dataMercados:
                        mercados.append(
                            {'cod_mercado': mercado['id_mercado'], 'nom_mercado': mercado['nom_mercado']}
                        )
                    empresa.append(
                        {
                            'cod_empresa': result[0],
                            'nom_empresa': result[1],
                            'servicio': result[2],
                            'mercados': mercados
                        }
                    )
        return empresa

    def __execute_query(self):
        # print("* EMPRESA -> ", self.__EMPRESA_ARG)
        # print("* MERCADO -> ", self.__MERCADO_ARG)
        # print("* QUERY -> ", self.__query)
        self.cursor.execute(self.__query, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        return self.cursor

    def getMercados(self):
        self.__upload_source_mercado()
        return self.__getDataMercado()

    def __upload_source_mercado(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/mercados.json"
        source = json.load(open(path + file))
        self.__query1 = ''.join(source["query"])

    def __getDataMercado(self):
        mercados = []
        data = self.__execute_query_mercado()
        for result in data:
            mercados.append({
                'id_mercado': result[0],
                'nom_mercado': result[1],
                'estado': result[2]
            })
        return mercados

    def __execute_query_mercado(self):
        self.cursor.execute(self.__query1, MERCADO_ARG=0)
        return self.cursor
