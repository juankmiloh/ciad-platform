from ....models.revisor.CostoUnitario import CostoUnitario
from ....models.revisor.Componente import Componente
from ....models.revisor.formulas.FormulaCpteP097 import FormulaCpteP097
from ....models.revisor.formulas.FormulaCpteD097 import FormulaCpteD097
import pandas as pd


class CostoUnitarioService(CostoUnitario):
    def __init__(self, anio, mes, empresa, mercado, ntprop):
        super().__init__(anio, mes, empresa, mercado, ntprop)

    def get_model_cu(self, dataCU):
        valuesCU = []
        componentes = []
        componenteG = Componente("G", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteT = Componente("T", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, self._CostoUnitario__NTPROP_ARG)
        componenteP015 = Componente("P015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteP097 = Componente("P097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteD015 = Componente("D015", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteD097 = Componente("D097", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteC = Componente("C", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")
        componenteR = Componente("R", self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, self._CostoUnitario__MERCADO_ARG, "No")

        cpteG = pd.DataFrame(componenteG.get_values_component_SUI())
        cpteT = pd.DataFrame(componenteT.get_values_component_SUI())
        cpteP015, numrowsCpteP015 = self.get_props_cpte(componenteP015)
        cpteP097 = componenteP097.get_values_component_SUI()
        cpteP097 = FormulaCpteP097().merge_perdidas_P097(pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5']))
        cpteD015, numrowsCpteD015 = self.get_props_cpte(componenteD015)
        cpteD097 = componenteD097.get_values_component_SUI()
        cpteD097 = FormulaCpteD097().merge_perdidas_D097(pd.DataFrame(cpteD097, columns=['ano','mes','empresa','mercado','c5']), self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG)
        cpteR = pd.DataFrame(componenteR.get_values_component_SUI())
        cpteC = pd.DataFrame(componenteC.get_values_component_SUI(), columns=['empresa','mercado','ano','mes','c6','c1','c13','c20','c22','c24','c21','c14','c15','c16','c23','c25','c28','c29','c30','c31','c32','c36','c34','c33','c37','c35','c38','c59','c69','c70','c71','c58','c60','c44','c47','c48','c55','c56','c52','c53'])

        for result in dataCU:
            # --------------------- VALORES CPTE G --------------------- #
            modelG = self.get_values_cpteG(cpteG, result)
            # --------------------- VALORES CPTE T --------------------- #
            modelT = self.get_values_cpteT(cpteT, result)
            # --------------------- VALORES CPTE P --------------------- #
            modelP = self.get_values_cpteP(numrowsCpteP015, cpteP015, cpteP097, result)
            # --------------------- VALORES CPTE D --------------------- #
            modelD = self.get_values_cpteD(numrowsCpteD015, cpteD015, cpteD097, result)
            # --------------------- VALORES CPTE R --------------------- #
            modelR = self.get_values_cpteR(cpteR, result)
            # --------------------- VALORES CPTE C --------------------- #
            modelC = self.get_values_cpteC(cpteC, result, self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG, modelG, modelT, modelP, modelD, modelR)
            # --------------------- VALORES CPTE CU --------------------- #
            modelCU = self.get_values_cpteCU(modelG, modelT, modelP, modelD, modelR, modelC, result)

            componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP, 'component_d': modelD, 'component_r': modelR, 'component_c': modelC, 'component_cu': modelCU}]
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