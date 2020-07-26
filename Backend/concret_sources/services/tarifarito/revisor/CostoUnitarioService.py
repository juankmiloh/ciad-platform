from ....models.revisor.CostoUnitario import CostoUnitario
from ....models.revisor.Componente import Componente
from ....models.revisor.formulas.FormulaCpteP097 import FormulaCpteP097
import pandas as pd

class CostoUnitarioService(CostoUnitario):
    def __init__(self, anio, mes, empresa, mercado, ntprop):
        super().__init__(anio, mes, empresa, mercado, ntprop)

    def get_model_cu(self, dataCU):
        return self.get_values_components(dataCU)

    def get_values_components(self, dataCU):
        valuesCU = []
        componentes = []
        componenteG = Componente("G", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteT = Componente("T", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, self._CostoUnitario__NTPROP_ARG)
        componenteP097 = Componente("P097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        # componenteP015 = Componente("P015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        
        cpteG = pd.DataFrame(componenteG.get_values_component_SUI())
        cpteT = pd.DataFrame(componenteT.get_values_component_SUI())
        cpteP097 = componenteP097.get_values_component_SUI()
        cpteP097 = FormulaCpteP097().merge_perdidas_P097(pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5']))
        # cpteP015 = pd.DataFrame(componenteP015.get_values_component_SUI())

        # print("------------------- 000015 ------------------")
        # print(cpteP015)

        for result in dataCU:
            find = (cpteG[21] == result[12]) & (cpteG[22] == result[1]) & (cpteG[19] == result[13]) & (cpteG[20] == result[14])
            calculado_g = cpteG.loc[find][33].tolist()[0]
            find = (cpteT[0] == result[12]) & (cpteT[1] == result[1]) & (cpteT[3] == result[13]) & (cpteT[4] == result[14]) & (cpteT[2] == result[4])
            calculado_t = cpteT.loc[find][6].tolist()[0]
            # EMPRESA - MERCADO - ANIO - PERIODO
            find = (cpteP097['empresa'] == result[12]) & (cpteP097['mercado'] == result[1]) & (cpteP097['ano'] == result[13]) & (cpteP097['mes'] == result[14])
            
            print("------------------- cpteP097 ------------------")
            print(find)

            if result[4].find('1') != -1:
                calculado_p = cpteP097['nt1'].tolist()[0]
            if result[4].find('2') != -1:
                calculado_p = cpteP097['nt2'].tolist()[0]
            if result[4].find('3') != -1:
                calculado_p = cpteP097['nt3'].tolist()[0]
            if result[4].find('4') != -1:
                calculado_p = cpteP097['nt4'].tolist()[0]

            # find = (cpteP015[2] == result[12]) & (cpteP097[3] == result[1]) & (cpteP097[0] == result[13]) & (cpteP097[1] == result[14])

            print("------------------- cpteP015 ------------------")
            print(find)          

            modelG = [{ 'value': "g", 'cpte_publicado': result[5], 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
            modelT = [{ 'value': "t", 'cpte_publicado': result[6], 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
            modelP097 = [{ 'value': "p", 'cpte_publicado': result[7], 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P097 publicado:', 'label_calculado': 'Componente P097 calculado:' }]
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
