import os
import glob
import json

PATH = os.path.dirname(os.path.realpath(__file__))

class Tools:
	__instance = None
	__search_dir_param = None
	
	@staticmethod
	def get_instance(param):
		if Tools.__instance == None:
			Tools.__search_dir_param = param
			Tools()
		return Tools.__instance 

	def __init__(self):
		if Tools.__instance == None:
			Tools.__instance = self

		#self.__search_dir = "Sources/pqrs_source/"
		self.__search_dir = Tools.__search_dir_param
		self.__sources = {}
		self.__source_load()

	def __source_load(self):
		files = self.__get_files()

		for file in files:
			with open( PATH + "/" + file) as file_json:
			    data_file = json.load(file_json)

			self.__sources[data_file["name"]] = data_file

 
	def __get_files(self):
		return filter(os.path.isfile, glob.glob(self.__search_dir + "*.json"))


	def get_source_by_name(self, name):
		return self.__sources.get(name,None)