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
        componenteP015 = Componente("P015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteP097 = Componente("P097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        
        cpteG = pd.DataFrame(componenteG.get_values_component_SUI())
        cpteT = pd.DataFrame(componenteT.get_values_component_SUI())
        cpteP015, numrowsCpteP015 = self.get_props_cpteP015(componenteP015)
        cpteP097 = componenteP097.get_values_component_SUI()
        cpteP097 = FormulaCpteP097().merge_perdidas_P097(pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5']))

        for result in dataCU:
            # --------------------- VALORES CPTE G --------------------- #
            # EMPRESA - MERCADO - ANIO - PERIODO
            find = (cpteG[21] == result[12]) & (cpteG[22] == result[1]) & (cpteG[19] == result[13]) & (cpteG[20] == result[14])
            calculado_g = cpteG.loc[find][33].tolist()[0]
            modelG = [{ 'value': "G", 'cpte_publicado': result[5], 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
            # --------------------- VALORES CPTE T --------------------- #
            find = (cpteT[0] == result[12]) & (cpteT[1] == result[1]) & (cpteT[3] == result[13]) & (cpteT[4] == result[14]) & (cpteT[2] == result[4])
            calculado_t = cpteT.loc[find][6].tolist()[0]
            modelT = [{ 'value': "T", 'cpte_publicado': result[6], 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
            # --------------------- VALORES CPTE P --------------------- #
            if numrowsCpteP015 > 0:
                # --------------------- VALORES CPTE P015 --------------------- #
                modelP = self.get_values_cpteP('P015', cpteP015, result)
            else:
                # --------------------- VALORES CPTE P097 --------------------- #
                modelP = self.get_values_cpteP('P097', cpteP097, result)

            componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP}]
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

    def get_props_cpteP015(self, cpte):
        df = pd.DataFrame(cpte.get_values_component_SUI())
        numRows = df.shape[0]
        return df, numRows

    def get_values_cpteP(self, cpte, data, result):
        # print("COMPONENTE | ", cpte, " | DATA | ", data, " | RESULT | ", result)
        if cpte == 'P015':
            # --------------------- VALORES CPTE P015 --------------------- #
            find = (data[2] == result[12]) & (data[3] == result[1]) & (data[0] == result[13]) & (data[1] == result[14])
            if result[4].find('1') != -1:
                publicado_p = result[7]
                calculado_p = data.loc[find][28].tolist()[0]
            if result[4].find('2') != -1:
                publicado_p = result[7]
                calculado_p = data.loc[find][29].tolist()[0]
            if result[4].find('3') != -1:
                publicado_p = result[7]
                calculado_p = data.loc[find][30].tolist()[0]
            if result[4].find('4') != -1:
                publicado_p = result[7]
                calculado_p = data.loc[find][31].tolist()[0]
            modelP = [{ 'value': "P015", 'cpte_publicado': publicado_p, 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P015 publicado:', 'label_calculado': 'Componente P015 calculado:' }]
        else:
            # --------------------- VALORES CPTE P097 --------------------- #
            find = (data['empresa'] == result[12]) & (data['mercado'] == result[1]) & (data['ano'] == result[13]) & (data['mes'] == result[14])
            if result[4].find('1') != -1:
                publicado_p = result[7]
                calculado_p = data['nt1'].tolist()[0]
            if result[4].find('2') != -1:
                publicado_p = result[7]
                calculado_p = data['nt2'].tolist()[0]
            if result[4].find('3') != -1:
                publicado_p = result[7]
                calculado_p = data['nt3'].tolist()[0]
            if result[4].find('4') != -1:
                publicado_p = result[7]
                calculado_p = data['nt4'].tolist()[0]
            modelP = [{ 'value': "P097", 'cpte_publicado': publicado_p, 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P097 publicado:', 'label_calculado': 'Componente P097 calculado:' }]
        return modelP