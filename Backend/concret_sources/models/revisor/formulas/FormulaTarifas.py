from ....util.ServiceConnection import serviceConnection
import pandas as pd
import numpy as np
import math

class FormulaTarifas(object):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def calcular_tarifas(self, dataframe, ano, mes):
        tarifas = dataframe

        # tarifas['juank'] = 123456

        #Consutla MongoDB GESTOR IDANE (trae solo IPC - mes anterior) - cuadrar para cuando sea diciembre
        tarifas['ipc_mes_anterior'] = self.__getIPC(ano, mes, 2)
        tarifas['ipc_mes_consultado'] = self.__getIPC(ano, mes, 1)

        # print('VALOR IF > ', (1 - (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])))
        # print('SI ES MENOR A 0.6 > ', (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8]))))
        # print('SI ES MAYOR A 0.6  > ', (tarifas[21] * (1 - 0.6)))

        # CALCULO TARIFAS ESTRATO 1
        tarifas.loc[(1 - (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) > 0.6, 'CT_E1'] = (tarifas[21] * (1 - 0.6))
        tarifas.loc[(1 - (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) <= 0.6, 'CT_E1'] = (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])))
        # print('---------------------------------tarifas -> ', tarifas['CT_E1'].isnull().values.any(), '-------------------------')

        if tarifas['CT_E1'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_E1'] = 0

        # CALCULO TARIFAS ESTRATO 2
        tarifas.loc[(1 - (tarifas[19] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) > 0.5, 'CT_E2'] = (tarifas[21] * (1 - 0.5))
        tarifas.loc[(1 - (tarifas[19] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) <= 0.5, 'CT_E2'] = (tarifas[19] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])))
        # tarifas.loc[np.isnan(tarifas['CT_E2']), 'CT_E2'] = 0 # Validamos si es NaN
        if tarifas['CT_E2'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_E2'] = 0

        # CALCULO TARIFAS ESTRATO 3
        tarifas['CT_E3'] = tarifas[21] * (1 - 0.15)
        # tarifas.loc[np.isnan(tarifas['CT_E3']), 'CT_E3'] = 0 # Validamos si es NaN
        if tarifas['CT_E3'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_E3'] = 0
        
        # CALCULO TARIFAS ESTRATO 5
        tarifas['CT_E5'] = tarifas[21] * (1.2)
        # tarifas.loc[np.isnan(tarifas['CT_E5']), 'CT_E5'] = 0 # Validamos si es NaN
        if tarifas['CT_E5'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_E5'] = 0
        
        # CALCULO TARIFAS ESTRATO 6
        tarifas['CT_E6'] = tarifas[21] * (1.2)
        # tarifas.loc[np.isnan(tarifas['CT_E6']), 'CT_E6'] = 0 # Validamos si es NaN
        if tarifas['CT_E6'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_E6'] = 0
        
        # CALCULO TARIFAS ESTRATO INDUSTRIAL
        tarifas['CT_INDUSTRIAL'] = tarifas[21] * (1.2)
        # tarifas.loc[np.isnan(tarifas['CT_INDUSTRIAL']), 'CT_INDUSTRIAL'] = 0 # Validamos si es NaN
        if tarifas['CT_INDUSTRIAL'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_INDUSTRIAL'] = 0
        
        # CALCULO TARIFAS ESTRATO COMERCIAL
        tarifas['CT_COMERCIAL'] = tarifas[21] * (1.2)
        # tarifas.loc[np.isnan(tarifas['CT_COMERCIAL']), 'CT_COMERCIAL'] = 0 # Validamos si es NaN
        if tarifas['CT_COMERCIAL'].isnull().values.any(): # Validamos si es NaN
            tarifas['CT_COMERCIAL'] = 0

        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 1
        tarifas['CPS_E1'] = (1 - tarifas['CT_E1'] / tarifas[21]) * 100
        # tarifas.loc[np.isnan(tarifas['CPS_E1']), 'CPS_E1'] = 0 # Validamos si es NaN
        if tarifas['CPS_E1'].isnull().values.any(): # Validamos si es NaN
            tarifas['CPS_E1'] = 0
        
        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 2
        tarifas['CPS_E2'] = (1 - tarifas['CT_E2'] / tarifas[21]) * 100
        # tarifas.loc[np.isnan(tarifas['CPS_E2']), 'CPS_E2'] = 0 # Validamos si es NaN
        if tarifas['CPS_E2'].isnull().values.any(): # Validamos si es NaN
            tarifas['CPS_E2'] = 0
        
        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 3
        tarifas['CPS_E3'] = (1 - tarifas['CT_E3'] / tarifas[21]) * 100
        # tarifas.loc[np.isnan(tarifas['CPS_E3']), 'CPS_E3'] = 0 # Validamos si es NaN
        if tarifas['CPS_E3'].isnull().values.any(): # Validamos si es NaN
            tarifas['CPS_E3'] = 0

        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 3
        tarifas['CPS_E4'] = 0

        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 3
        tarifas['CPS_E5'] = 0

        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 3
        tarifas['CPS_E6'] = 0

        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 3
        tarifas['CPS_INDUSTRIAL'] = 0

        # CALCULO PORCENTAJE SUBSIDIOS ESTRATO 3
        tarifas['CPS_COMERCIAL'] = 0
        
        print('data TARIFAS -> ', tarifas)

        return tarifas

    def __getIPC(self, ano, periodo, mes):
        MES_ARG = self.meses[int(periodo) - mes] # m-1 ó mes consultado
        result = list(self.connMDB.indicesDANE.find({"anio": ano}, {'meses.' + MES_ARG: 1 }))
        key_mes = []
        for x in result:
            for key, value in x['meses'].items():
                key_mes.append(key)

        obj = []

        for m in key_mes:
            result_mes = result[0]['meses'][m]
            ipc = result_mes[len(result_mes)-1]['ipc']
        return ipc