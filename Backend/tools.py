import os
import glob
import json

PATH = os.path.dirname(os.path.realpath(__file__))

class Tools:
	__instance = None
	
	@staticmethod
	def get_instance():
		if Tools.__instance == None:
			Tools()
		return Tools.__instance 

	def __init__(self):
		if Tools.__instance == None:
			Tools.__instance = self

		self.__search_dir = "Sources/"
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