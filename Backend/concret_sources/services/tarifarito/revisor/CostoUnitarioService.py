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
            modelD = self.get_values_cpteD(self.myDict['D015'], self.myDict['D097'], result, self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG)
            # --------------------- VALORES CPTE R --------------------- #
            modelR = self.get_values_cpteR(self.myDict['R'], result)
            # --------------------- VALORES CPTE C --------------------- #
            modelC = self.get_values_cpteC(self.myDict['C'], result, self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG)
            # --------------------- VALORES CPTE CU --------------------- #
            modelCU = self.get_values_cpteCU(modelG, modelT, modelP, modelD, modelR, modelC, result)

            componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP, 'component_d': modelD, 'component_r': modelR, 'component_c': modelC, 'component_cu': modelCU}]
            # componentes = [{'component_g': modelG, 'component_t': modelT, 'component_r': modelR}]
            valuesCU.append({
                    'id_empresa': result[12],
                    'id_mercado': result[1],
                    'mercado': result[18],
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
        componenteG = Componente("G", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteT = Componente("T", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, self._CostoUnitario__NTPROP_ARG)
        componenteP015 = Componente("P015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteP097 = Componente("P097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteD015 = Componente("D015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteD097 = Componente("D097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteR = Componente("R", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteC = Componente("C", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")

        t1 = threading.Thread(target=self.get_values, args=({'key': 'G', 'values': componenteG},)) 
        t2 = threading.Thread(target=self.get_values, args=({'key': 'T', 'values': componenteT},))
        t3 = threading.Thread(target=self.get_values, args=({'key': 'P015', 'values': componenteP015},))
        t4 = threading.Thread(target=self.get_values, args=({'key': 'P097', 'values': componenteP097},))
        t5 = threading.Thread(target=self.get_values, args=({'key': 'D015', 'values': componenteD015},))
        t6 = threading.Thread(target=self.get_values, args=({'key': 'D097', 'values': componenteD097},))
        t7 = threading.Thread(target=self.get_values, args=({'key': 'R', 'values': componenteR},))
        t8 = threading.Thread(target=self.get_values, args=({'key': 'C', 'values': componenteC},))

        # starting thread 8
        t8.start()
        # starting thread 6
        t6.start()
        # starting thread 2
        t2.start()
        # starting thread 3
        t3.start()
        # starting thread 4
        t4.start()
        # starting thread 5
        t5.start()
        # starting thread 1
        t1.start()
        # starting thread 7
        t7.start()

        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
        # wait until thread 3 is completely executed
        t3.join()
        # wait until thread 4 is completely executed
        t4.join()
        # wait until thread 5 is completely executed
        t5.join()
        # wait until thread 6 is completely executed
        t6.join()
        # wait until thread 7 is completely executed
        t7.join()
        # wait until thread 8 is completely executed
        t8.join()

        # todos threads completely executed
        print("Done!")
        print(f"finished at {time.strftime('%X')}")

    def get_values(self, cpte):
        # print('CPTE > ', cpte['key'])
        if cpte['key'] == 'P097':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5'])
        elif cpte['key'] == 'D097':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['ano','mes','empresa','mercado','c5'])
        elif cpte['key'] == 'C':
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI(), columns=['empresa','mercado','ano','mes','c6','c1','c7','c8','c9','c10','c11','c13','c20','c22','c24','c21','c14','c15','c16','c23','c25','c28','c29','c30','c31','c32','c36','c34','c33','c37','c35','c38','c59','c69','c70','c71','c58','c60','c44','c47','c48','c55','c56','c52','c53'])
        else:
            self.myDict[cpte['key']] = pd.DataFrame(cpte['values'].get_values_component_SUI())