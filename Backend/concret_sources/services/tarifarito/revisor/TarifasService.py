from ....models.revisor.Tarifas import Tarifas
import pandas as pd
import asyncio
import time
import threading


class TarifasService(Tarifas):
    def __init__(self, anio, mes, empresa, mercado, ntprop):
        super().__init__(anio, mes, empresa, mercado, ntprop)

    def get_model_tarifas(self, dataTarifas):
        print(f"started at {time.strftime('%X')}")
        valuesTarifas = []
        tarifas = []
        self.data = dataTarifas
        calculoTarifas = self.get_values_tarifas(pd.DataFrame(self.data), self._Tarifas__ANIO_ARG, self._Tarifas__PERIODO_ARG)

        for result in self.data:
            # --------------------- VALORES CALCULO TARIFAS / ESTRATOS --------------------- #
            # calculoTarifas = self.get_values_tarifas(pd.DataFrame(self.data), result)

            tarifas = [{'ESTRATO 1': calculoTarifas['estrato1'], 'ESTRATO 2': calculoTarifas['estrato2'], 'ESTRATO 3': calculoTarifas['estrato3'], 'ESTRATO 4': calculoTarifas['estrato4'], 'ESTRATO 5': calculoTarifas['estrato5'], 'ESTRATO 6': calculoTarifas['estrato6'], 'INDUSTRIAL': calculoTarifas['industrial'], 'COMERCIAL': calculoTarifas['comercial']}]
            
            valuesTarifas.append({
                'id_empresa': result[0],
                'id_mercado': result[1],
                'ano': result[2],
                'mes': result[3],
                'nt_prop': result[4],
                'tarifas': tarifas
            })
            tarifas = []
        return valuesTarifas
