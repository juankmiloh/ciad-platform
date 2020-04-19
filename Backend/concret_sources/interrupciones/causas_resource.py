from ..config.oracle_connection import OracleConnection
from tools import Tools
from flask import request
from flask_restful import Resource

class CausasInterrupcion(Resource):
	def get(self, causa=0):
		self.__CAUSA_ARG = causa if causa != 0 else 0
		self.__upload_source()
		return self.__getData()

	def __upload_source(self):
		tools = Tools.get_instance("Sources/interrupciones/")
		source = tools.get_source_by_name("causas")
		self.__set_source(source)


	def __set_source(self, source):
		self.__name = source["name"] # nombre del json
		self.__query = ''.join(source["query"]) #query que se quiere hacer y se concatena porque es un string

	def __getData(self):
		causas = []
		data = self.__execute_query()
		for result in data:
			causas.append(
				{
					'cod_causa' : result[0],
					'col_sui' : result[1],
					'descripcion' : result[2]
				}
			)
		return causas

	def __execute_query(self):
		oracleConnection = OracleConnection()
		connection = oracleConnection.get_connection()
		cursor = connection.cursor()
		print("________CAUSA____________")
		print(self.__CAUSA_ARG)
		print("____________________________")
		print("_________QUERY______________")
		print("SQL:", self.__query)
		print("____________________________")
		cursor.execute(self.__query, CAUSA_ARG = self.__CAUSA_ARG)
		return cursor