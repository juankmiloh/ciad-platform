from ...config.oracle_connection import OracleConnection
from tools import Tools
from flask import request
from flask_restful import Resource


class mercadosTarifarito(Resource):
    def get(self, comercializador=0):
        self.__COMERC_ARG = comercializador if comercializador != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        tools = Tools.get_instance("Sources/tarifarito/")
        source = tools.get_source_by_name("mercados")
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        mercados = []
        data = self.__execute_query()
        for result in data:
            mercados.append(
                {
                    'id_mercado': result[0],
                }
            )
        return mercados

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________EMPRESA____________")
        print(self.__COMERC_ARG)
        print("____________________________")
        print("_________QUERY______________")
        print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, COMERC_ARG=self.__COMERC_ARG)
        return cursor
