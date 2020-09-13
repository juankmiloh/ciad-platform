from .....util.ServiceConnection import serviceConnection
from .....services.tarifarito.revisor.ComponentService import ComponentService
from flask import request
from flask_restful import Resource
import os
import json


class rComponentR(Resource):
    def __init__(self):
        self.connection = serviceConnection()
    
    def get(self, anio=0, mes=0, empresa=0, mercado=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        componentService = ComponentService("R", self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, "No")
        dataCpte = componentService.get_values_component_SUI()
        jsonValues = componentService.get_model_component(dataCpte)
        return jsonValues

    def post(self):
        self.connMDB = self.connection.get_connectionMDB()
        req = request.args.get('params')
        self.connMDB.componentes.insert_one(
            json.loads(req)
        )
        return req