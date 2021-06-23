from ....models.revisor.CostoUnitario import CostoUnitario
from ....models.revisor.Componente import Componente
import pandas as pd
import asyncio
import time
import threading


class CostoUnitarioService(CostoUnitario):
    def __init__(self, anio, mes, empresa, mercado, ntprop):
        super().__init__(anio, mes, empresa, mercado, ntprop)

    def get_model_cu(self, dataCU):
        valuesCU = []
        componentes = []
        self.init_componentes()

        for result in dataCU:
            # --------------------- VALORES CPTE G --------------------- #
            modelG = self.get_values_cpteG(self.myDict['G'], result)
            # --------------------- VALORES CPTE T --------------------- #
            modelT = self.get_values_cpteT(self.myDict['T'], result)
            # --------------------- VALORES CPTE P --------------------- #
            modelP = self.get_values_cpteP(self.myDict['P015'], self.myDict['P097'], result)
            # --------------------- VALORES CPTE D --------------------- #
            modelD, numrowsCpteD015 = self.get_values_cpteD(self.myDict['D015'], self.myDict['D097'], result, self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG)
            # --------------------- VALORES CPTE DTUN --------------------- #
            modelDtun = self.get_values_cpteDtun(self.myDict['DTUN'], result)
            # --------------------- VALORES CPTE R --------------------- #
            modelR = self.get_values_cpteR(self.myDict['R'], result)
            # --------------------- VALORES CPTE C --------------------- #
            modelC = self.get_values_cpteC(self.myDict['C'], result, self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG)
            # --------------------- VALORES CPTE CU --------------------- #
            modelCU = self.get_values_cpteCU(modelG, modelT, modelP, modelD, modelR, modelC, result)

            if numrowsCpteD015 > 0:
                componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP, 'component_d': modelD, 'component_dtun': modelDtun, 'component_r': modelR, 'component_c': modelC, 'component_cu': modelCU}]
            else:
                componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP, 'component_d': modelD, 'component_r': modelR, 'component_c': modelC, 'component_cu': modelCU}]
            valuesCU.append({
                'id_empresa': result[12],
                'id_mercado': result[1],
                'mercado': result[20],
                'ano': result[13],
                'mes': result[14],
                'nt_prop': result[4],
                'componentes': componentes
            })
            componentes = []
        return valuesCU

    def init_componentes(self):
        print(f"started at {time.strftime('%X')}")
        self.myDict = {}
        self.myDictCpte = {}
        componenteG = Componente("G", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteT = Componente("T", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, self._CostoUnitario__NTPROP_ARG)
        componenteP015 = Componente("P015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteP097 = Componente("P097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteD015 = Componente("D015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteD097 = Componente("D097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteDtun = Componente("DTUN", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteR = Componente("R", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteC = Componente("C", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")

        self.myDictCpte['cpteG'] = threading.Thread(target=self.get_values, args=({'key': 'G', 'values': componenteG},)) 
        self.myDictCpte['cpteT'] = threading.Thread(target=self.get_values, args=({'key': 'T', 'values': componenteT},))
        self.myDictCpte['cpteP015'] = threading.Thread(target=self.get_values, args=({'key': 'P015', 'values': componenteP015},))
        self.myDictCpte['cpteP097'] = threading.Thread(target=self.get_values, args=({'key': 'P097', 'values': componenteP097},))
        self.myDictCpte['cpteD015'] = threading.Thread(target=self.get_values, args=({'key': 'D015', 'values': componenteD015},))
        self.myDictCpte['cpteD097'] = threading.Thread(target=self.get_values, args=({'key': 'D097', 'values': componenteD097},))
        self.myDictCpte['cpteDtun'] = threading.Thread(target=self.get_values, args=({'key': 'DTUN', 'values': componenteDtun},))
        self.myDictCpte['cpteR'] = threading.Thread(target=self.get_values, args=({'key': 'R', 'values': componenteR},))
        self.myDictCpte['cpteC'] = threading.Thread(target=self.get_values, args=({'key': 'C', 'values': componenteC},))

        # starting thread
        for cpte in self.myDictCpte:
            self.myDictCpte[cpte].start()

        # wait until thread is completely executed
        for cpte in self.myDictCpte:
            self.myDictCpte[cpte].join()

        # All threads completely executed
        print("Done!")
        print(f"finished at {time.strftime('%X')}")

    def get_values(self, cpte):
        # print('CPTE > ', cpte['key'])
        if cpte['key'] == 'P097':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5'])
        elif cpte['key'] == 'D097':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['ano','mes','empresa','mercado','c5'])
        elif cpte['key'] == 'DTUN':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['ano','mes','empresa','c2','c7','ADD','c1','c5','c6','c3','c4'])
        elif cpte['key'] == 'C':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['empresa','mercado','ano','mes','c6','c1','c7','c8','c9','c10','c11','c13','c20','c22','c24','c21','c14','c15','c16','c23','c25','c28','c29','c30','c31','c32','c36','c34','c33','c37','c35','c38','c59','c69','c70','c71','c58','c60','c44','c47','c48','c55','c56','c52','c53'])
        else:
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI())