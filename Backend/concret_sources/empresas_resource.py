import datetime
import csv

from flask import send_from_directory
from flask import send_file #descargar archivos

from tools import Tools
from flask import request
from flask_restful import Resource
from .config.oracle_connection import OracleConnection

class EmpresasRsource(Resource):
	def get(self, servicio = ""):

		self.__SERVICIO_ARG = servicio if servicio != "" else "TODOS"
		self.__SERVICIO_ARG = self.__SERVICIO_ARG.upper()

		self.__upload_source()

		return self.__getData()

	def __upload_source(self):
		tools = Tools.get_instance()
		source = tools.get_source_by_name("empresas")
		self.__set_source(source)

	def __set_source(self, source):
		self.__name = source["name"] # nombre del json
		self.__query = ''.join(source["query"]) #query que se quiere hacer y se concatena porque es un string

	def __getData(self):
		empresas = []
		data = self.__execute_query()

		for pqr in data:
			empresas.append(
				{
					'cod_empresa' : pqr[0],
					'nombre' : pqr[1],
					'servicio' : pqr[2],
				}
			)

		return empresas

	def __execute_query(self):
		oracleConnection = OracleConnection()
		connection = oracleConnection.get_connection()
		cursor = connection.cursor()

		print("____________________________")
		print(self.__SERVICIO_ARG)
		print("____________________________")

		print("____________________________")
		print("SQL:", self.__query)
		print("____________________________")

		cursor.execute(self.__query, SERVICIO_ARG = self.__SERVICIO_ARG)

		return cursor
