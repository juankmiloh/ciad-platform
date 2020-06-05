import datetime
import csv

from flask import send_from_directory
from flask import send_file #descargar archivos

from tools import Tools
from flask import request
from flask_restful import Resource
from ...config.oracle_connection import OracleConnection

class AniosRsource(Resource):
	def get(self, anio = 0):

		now = datetime.datetime.now()
		self.__ANIO_ARG = anio if anio != 0 else 0

		self.__upload_source()

		return self.__getData()

	def __upload_source(self):
		tools = Tools.get_instance("Sources/pqrs/")
		source = tools.get_source_by_name("anios")
		self.__set_source(source)

	def __set_source(self, source):
		self.__name = source["name"] # nombre del json
		self.__query = ''.join(source["query"]) #query que se quiere hacer y se concatena porque es un string

	def __getData(self):	

		anios = []

		if self.__ANIO_ARG != 0: # se ejecuta cuando se envia el año
			print("________Se recibe año________________")
			print(self.__ANIO_ARG)
			print("____________________________")

			data = self.__execute_query()

			for pqr in data:
				anios.append(
					{
						'anio' : pqr[0],
						'mes' : pqr[1]
					}
				)
			
			return anios
		else: # se ejecuta cuando se quieren obtener todos los años
			print("________No se recibe año________________")
			print(self.__ANIO_ARG)
			print("____________________________")

			data = self.__execute_query()

			anio = 0		

			for pqr in data:

				if anio != pqr[0]:
					anios.append(
						{
							'anio' : pqr[0]
						}
					)
				anio = pqr[0]
				
			return anios

		

	def __execute_query(self):
		oracleConnection = OracleConnection()
		connection = oracleConnection.get_connection()
		cursor = connection.cursor()

		print("________ANIO________________")
		print(self.__ANIO_ARG)
		print("____________________________")
		
		print("_________QUERY______________")
		print("SQL:", self.__query)
		print("____________________________")

		cursor.execute(self.__query, ANIO_ARG = self.__ANIO_ARG)

		return cursor
