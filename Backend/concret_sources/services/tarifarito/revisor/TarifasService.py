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

        for result in dataTarifas:
            tarifas = [{'ESTRATO 1': result[5], 'ESTRATO 2': result[6], 'ESTRATO 3': result[7], 'ESTRATO 4': result[8], 'ESTRATO 5': result[9], 'ESTRATO 6': result[10], 'INDUSTRIAL': result[11], 'COMERCIAL': result[12]}]
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