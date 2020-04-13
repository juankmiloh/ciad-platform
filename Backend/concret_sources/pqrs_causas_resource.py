import datetime
import csv

from flask import send_from_directory
from flask import send_file #descargar archivos

from tools import Tools
from flask import request
from flask_restful import Resource
from .config.oracle_connection import OracleConnection

class PqrsCausasRsource(Resource):
	def get(self, anio = 0, mes = 0, servicio = "", empresa = 0, causa=0):

		now = datetime.datetime.now()
		self.__ANIO_ARG = now.year if anio == 0 else anio
		# self.__ANIO_ARG = 2018
		self.__PERIODO_ARG = 0 if mes <= 0 else mes
		self.__SERVICIO_ARG = servicio if servicio != "" else "TODOS"
		self.__SERVICIO_ARG = self.__SERVICIO_ARG.upper()
		self.__EMPRESA_ARG = empresa if empresa != 0 else 0
		self.__CAUSA_ARG = causa if causa != 0 else 0

		self.__upload_source()

		return self.__getData()


	def __upload_source(self):
		tools = Tools.get_instance()
		source = tools.get_source_by_name("pqrs_causas")
		self.__set_source(source)


	def __set_source(self, source):
		self.__name = source["name"] # nombre del json
		self.__query = ''.join(source["query"]) #query que se quiere hacer y se concatena porque es un string
		#print(self.__query)


	def __getData(self):
		pqrs_causas = []
		data = self.__execute_query()

		for pqr in data:
			pqrs_causas.append(
				{
					'servicio' : pqr[0],
					'cod_causa' : pqr[1],
					'desc_causa' : pqr[2],					
					'numero_pqrs' : pqr[3]
				}
			)

		with open('file_pqrs.csv', 'w') as csvfile:
		    fieldnames = ['servicio', 'cod_causa', 'desc_causa', 'numero_pqrs']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		    writer.writeheader()
		    writer.writerows(pqrs_causas)

		print("writing pqrs complete")

		return pqrs_causas

		# return send_file('file_pqrs.csv', as_attachment=True)


	def __execute_query(self):
		oracleConnection = OracleConnection()
		connection = oracleConnection.get_connection()
		cursor = connection.cursor()

		print("________ANIO________________")
		print(self.__ANIO_ARG)
		print("____________________________")

		print("________MES_________________")
		print(self.__PERIODO_ARG)
		print("____________________________")

		print("________SERVICIO____________")
		print(self.__SERVICIO_ARG)
		print("____________________________")

		print("________EMPRESA_____________")
		print(self.__EMPRESA_ARG)
		print("____________________________")

		print("________CAUSA_______________")
		print(self.__CAUSA_ARG)
		print("____________________________")

		print("____________________________")
		print("SQL:", self.__query)
		print("____________________________")

		cursor.execute(self.__query, ANIO_ARG = self.__ANIO_ARG, PERIODO_ARG = self.__PERIODO_ARG, SERVICIO_ARG = self.__SERVICIO_ARG, EMPRESA_ARG = self.__EMPRESA_ARG, CAUSA_ARG = self.__CAUSA_ARG)

		return cursor
