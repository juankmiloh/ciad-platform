from .....util.ServiceConnection import serviceConnection
from .....services.tarifarito.revisor.ComponentService import ComponentService
from .....models.revisor.formulas.FormulaCpteC import FormulaCpteC
from flask import request
from flask_restful import Resource
import os
import json
import pandas as pd


class rComponentC(Resource):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
    
    def get(self, anio=0, mes=0, empresa=0, mercado=0, ntprop=""):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__NTPROP_ARG = ntprop if ntprop != "" else "TODOS"
        componentService = ComponentService("C", self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, self.__NTPROP_ARG)
        dataCpte = componentService.get_values_component_SUI()
        valuesCpte = FormulaCpteC().merge_comercializacion(pd.DataFrame(dataCpte, columns=['empresa','mercado','ano','mes','nt_prop','c6','c1','c7','c8','c9','c10','c11','c13','c20','c22','c24','c21','c14','c15','c16','c23','c25','c28','c29','c30','c31','c32','c36','c34','c33','c37','c35','c38','c59','c57','c58','c60','c44','c47','c48','c52','c53','c55','c56']), self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG)
        print('jsonValues', valuesCpte)
        jsonValues = componentService.get_model_component(valuesCpte)
        return jsonValues

    def post(self):
        req = request.args.get('params')
        self.connMDB.componentes.insert_one(
            json.loads(req)
        )
        return req