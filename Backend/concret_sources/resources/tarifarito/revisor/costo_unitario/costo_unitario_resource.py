from flask import request
from flask_restful import Resource
import os
import json
import pandas as pd
from .....models.revisor.CostoUnitario import CostoUnitario
from .....models.revisor.Componente import Componente


class rCostoUnitario(Resource):

    def get(self, anio=0, mes=0, empresa=0, mercado=0, ntprop=""):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__NTPROP_ARG = ntprop if ntprop != "" else "TODOS"
        cu = CostoUnitario(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, self.__NTPROP_ARG)
        self.dataCU = cu.getCostoUnitario()
        return self.__getComponentes()

    def __getComponentes(self):
        valuesCU = []
        componentes = []
        componenteG = Componente("G", self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, "No")
        componenteT = Componente("T", self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, self.__NTPROP_ARG)
        componenteP097 = Componente("P097", self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, "No")
        cpteG = componenteG.get_component_cu()
        cpteG = pd.DataFrame(cpteG)
        cpteT = componenteT.get_component_cu()
        cpteT = pd.DataFrame(cpteT)
        cpteP097 = componenteP097.get_component_cu()
        cpteP097 = componenteP097.merge_perdidas_P097(pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5']))
        for result in self.dataCU:
            find = (cpteG[21] == result[12]) & (cpteG[22] == result[1]) & (cpteG[19] == result[13]) & (cpteG[20] == result[14])
            calculado_g = cpteG.loc[find][33].tolist()[0]
            find = (cpteT[0] == result[12]) & (cpteT[1] == result[1]) & (cpteT[3] == result[13]) & (cpteT[4] == result[14]) & (cpteT[2] == result[4])
            calculado_t = cpteT.loc[find][6].tolist()[0]
            # EMPRESA - MERCADO - ANIO - PERIODO
            find = (cpteP097['empresa'] == result[12]) & (cpteP097['mercado'] == result[1]) & (cpteP097['ano'] == result[13]) & (cpteP097['mes'] == result[14])

            if result[4].find('1') != -1:
                calculado_p097_nt = cpteP097['nt1'].tolist()[0]
            if result[4].find('2') != -1:
                calculado_p097_nt = cpteP097['nt2'].tolist()[0]
            if result[4].find('3') != -1:
                calculado_p097_nt = cpteP097['nt3'].tolist()[0]
            if result[4].find('4') != -1:
                calculado_p097_nt = cpteP097['nt4'].tolist()[0]

            modelG = [{ 'value': "g", 'cpte_publicado': result[5], 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
            modelT = [{ 'value': "t", 'cpte_publicado': result[6], 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
            modelP097 = [{ 'value': "p", 'cpte_publicado': result[7], 'cpte_calculado': calculado_p097_nt, 'label_publicado': 'Componente P097 publicado:', 'label_calculado': 'Componente P097 calculado:' }]
            componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP097}]
            valuesCU.append({
                    'id_empresa': result[12],
                    'id_mercado': result[1],
                    'mercado': result[18],
                    'ano': result[13],
                    'mes': result[14],
                    'nt_prop': result[4],
                    'componentes': componentes,
                    # 'GM': result[5],
                    # 'TM': result[6],
                    # 'PRNM': result[7],
                    # 'DNM': result[8],
                    # 'CVM': result[9],
                    # 'RM': result[10],
                    # 'CUVM': result[11]
                })
            componentes = []
        return valuesCU