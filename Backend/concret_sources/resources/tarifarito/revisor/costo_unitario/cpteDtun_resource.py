from .....util.ServiceConnection import serviceConnection
from .....services.tarifarito.revisor.ComponentService import ComponentService
from .....models.revisor.formulas.FormulaCpteDtun import FormulaCpteDtun
from flask import request
from flask_restful import Resource
import os
import json
import pandas as pd


class rComponentDtun(Resource):
    def __init__(self):
        self.connection = serviceConnection()
    
    def get(self, anio=0, mes=0, empresa=0, mercado=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        componentService = ComponentService("DTUN", self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, "No")
        dataCpte = componentService.get_values_component_SUI()
        valuesCpte = FormulaCpteDtun().merge_perdidas_Dtun(pd.DataFrame(dataCpte, columns=['ano','mes','empresa','c2','c7','ADD','c1','c5','c6','c3','c4']), self.__MERCADO_ARG)
        jsonValues = componentService.get_model_component(valuesCpte)
        return jsonValues

    def post(self):
        self.connMDB = self.connection.get_connectionMDB()
        req = request.args.get('params')
        self.connMDB.componentes.insert_one(
            json.loads(req)
        )
        return req