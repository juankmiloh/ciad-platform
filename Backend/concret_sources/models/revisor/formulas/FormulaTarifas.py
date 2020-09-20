from ....util.ServiceConnection import serviceConnection
import pandas as pd
import numpy as np

class FormulaTarifas(object):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def calcular_tarifas(self, dataframe, ano, mes):
        tarifas = dataframe

        # tarifas['juank'] = 123456

        #Consutla MongoDB IDANE (trae solo IPC - mes anterior) - cuadrar para cuando sea diciembre
        tarifas['ipc_mes_anterior'] = self.__getIPC(ano, mes, 2)
        tarifas['ipc_mes_consultado'] = self.__getIPC(ano, mes, 1)

        # print('MIN > ', min((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), 1))
        print('MIN > ', np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])))

        tarifas.loc[(1 - (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) <= 0.6, 'TC_E1'] = tarifas['TC_E1'] = (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8]))) 
        tarifas.loc[(1 - (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) > 0.6, 'TC_E1'] = tarifas['TC_E1'] = (tarifas[21] * (1 - 0.6))
        # print('MIN > ', tarifas[['ipc_mes_consultado / ipc_mes_anterior','ipc_mes_consultado']].min(axis = 1))
        # if (1 - (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])) / tarifas[21])) <= 0.6:
        #     tarifas['TC_E1'] = (tarifas[18] * np.minimum((tarifas['ipc_mes_consultado'] / tarifas['ipc_mes_anterior']), (tarifas[21] / tarifas[8])))
        # else:
        #     tarifas['TC_E1'] = (tarifas[21] * (1 - 0.6))

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