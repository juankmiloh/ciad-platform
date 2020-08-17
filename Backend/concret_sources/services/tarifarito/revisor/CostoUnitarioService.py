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

        cpteG = pd.DataFrame(componenteG.get_values_component_SUI())
        cpteT = pd.DataFrame(componenteT.get_values_component_SUI())
        cpteP015, numrowsCpteP015 = self.get_props_cpte(componenteP015)
        cpteP097 = componenteP097.get_values_component_SUI()
        cpteP097 = FormulaCpteP097().merge_perdidas_P097(pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5']))
        cpteD015, numrowsCpteD015 = self.get_props_cpte(componenteD015)
        cpteD097 = componenteD097.get_values_component_SUI()
        cpteD097 = FormulaCpteD097().merge_perdidas_D097(pd.DataFrame(cpteD097, columns=['ano','mes','empresa','mercado','c5']), self._CostoUnitario__ANIO_ARG, self._CostoUnitario__PERIODO_ARG, self._CostoUnitario__EMPRESA_ARG)

        for result in dataCU:
            # --------------------- VALORES CPTE G --------------------- #
            modelG = self.get_values_cpteG(cpteG, result)
            # --------------------- VALORES CPTE T --------------------- #
            modelT = self.get_values_cpteT(cpteT, result)
            # --------------------- VALORES CPTE P --------------------- #
            modelP = self.get_values_cpteP(numrowsCpteP015, cpteP015, cpteP097, result)
            # --------------------- VALORES CPTE D --------------------- #
            modelD = self.get_values_cpteD(numrowsCpteD015, cpteD015, cpteD097, result)

            componentes = [{'component_g': modelG, 'component_t': modelT, 'component_p': modelP, 'component_d': modelD}]
            valuesCU.append({
                    'id_empresa': result[12],
                    'id_mercado': result[1],
                    'mercado': result[18],
                    'ano': result[13],
                    'mes': result[14],
                    'nt_prop': result[4],
                    'componentes': componentes,
                    # 'DNM': result[8],
                    # 'CVM': result[9],
                    # 'RM': result[10],
                    # 'CUVM': result[11]
                })
            componentes = []
        return valuesCU