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
        
        for index, row in calculoTarifas.iterrows(): 
            # print("Total income in "+ row["Date"]+ " is:"+str(row["Income_1"]+row["Income_2"]))
            # --------------------- VALORES CALCULO TARIFAS / ESTRATOS --------------------- #
            estrato1 = [{ 'value': "estrato1", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            estrato2 = [{ 'value': "estrato2", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            estrato3 = [{ 'value': "estrato3", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            # estrato4 = [{ 'value': "estrato1", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            estrato5 = [{ 'value': "estrato5", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            estrato6 = [{ 'value': "estrato6", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            industrial = [{ 'value': "industrial", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]
            comercial = [{ 'value': "comercial", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'porcentaje_subsidio': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'label_porcentaje': 'Porcentaje subsidio:', }]

            # tarifas = [{'ESTRATO 1': estrato1 }]
            tarifas = [{'ESTRATO 1': estrato1, 'ESTRATO 2': estrato2, 'ESTRATO 3': estrato3, 'ESTRATO 5': estrato5, 'ESTRATO 6': estrato6, 'INDUSTRIAL': industrial, 'COMERCIAL': comercial }]
            
            valuesTarifas.append({
                'id_empresa': row[0],
                'id_mercado': row[1],
                'ano': row[2],
                'mes': row[3],
                'nt_prop': row[4],
                'tarifas': tarifas
            })
            tarifas = []
        return valuesTarifas
