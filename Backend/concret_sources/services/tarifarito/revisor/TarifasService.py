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
            estrato1 = [{ 'value': "estrato1", 'tarifa_mes_anterior': row[5], 'tarifa_publicada': row[18], 'tarifa_calculada': row["CT_E1"], 'por_subsidio_publicado': row[31], 'por_subsidio_calculado': row["CPS_E1"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            estrato2 = [{ 'value': "estrato2", 'tarifa_mes_anterior': row[6], 'tarifa_publicada': row[19], 'tarifa_calculada': row["CT_E2"], 'por_subsidio_publicado': row[32], 'por_subsidio_calculado': row["CPS_E2"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            estrato3 = [{ 'value': "estrato3", 'tarifa_mes_anterior': row[7], 'tarifa_publicada': row[20], 'tarifa_calculada': row["CT_E3"], 'por_subsidio_publicado': row[33], 'por_subsidio_calculado': row["CPS_E3"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            # estrato4 = [{ 'value': "estrato1", 'tarifa_mes_anterior': row[8], 'tarifa_publicada': row[21], 'tarifa_calculada': row["CT_E4"], 'por_subsidio_publicado': row[34], 'por_subsidio_calculado': row["CPS_E4"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            estrato5 = [{ 'value': "estrato5", 'tarifa_mes_anterior': row[9], 'tarifa_publicada': row[22], 'tarifa_calculada': row["CT_E5"], 'por_subsidio_publicado': row[35], 'por_subsidio_calculado': row["CPS_E5"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            estrato6 = [{ 'value': "estrato6", 'tarifa_mes_anterior': row[10], 'tarifa_publicada': row[23], 'tarifa_calculada': row["CT_E6"], 'por_subsidio_publicado': row[36], 'por_subsidio_calculado': row["CPS_E6"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            industrial = [{ 'value': "industrial", 'tarifa_mes_anterior': row[11], 'tarifa_publicada': row[24], 'tarifa_calculada': row["CT_INDUSTRIAL"], 'por_subsidio_publicado': row[37], 'por_subsidio_calculado': row["CPS_INDUSTRIAL"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]
            comercial = [{ 'value': "comercial", 'tarifa_mes_anterior': row[12], 'tarifa_publicada': row[25], 'tarifa_calculada': row["CT_COMERCIAL"], 'por_subsidio_publicado': row[38], 'por_subsidio_calculado': row["CPS_COMERCIAL"], 'label_anterior': 'Tarifa mes anterior:', 'label_publicado': 'Tarifa publicada:', 'label_calculado': 'Tarifa calculada:', 'lbl_porcen_publicado': 'Porcentaje subsidio publicado', 'lbl_porcen_calculado': 'Porcentaje subsidio calculado' }]

            # tarifas = [{'Estrato 1': estrato1 }]
            tarifas = [{'Estrato 1': estrato1, 'Estrato 2': estrato2, 'Estrato 3': estrato3, 'Estrato 5': estrato5, 'Estrato 6': estrato6, 'Industrial': industrial, 'Comercial': comercial }]
            
            valuesTarifas.append({
                'id_empresa': row[0],
                'id_mercado': row[1],
                "mercado": row[40],
                'ano': row[2],
                'mes': row[16],
                'nt_prop': row[4],
                'tarifas': tarifas
            })
            tarifas = []
        return valuesTarifas
