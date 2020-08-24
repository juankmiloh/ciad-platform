from ....util.ServiceConnection import serviceConnection
import pandas as pd

class FormulaCpteC(object):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def merge_comercializacion(self, dataFrame, ano, mes, empresa):
        cpteC = dataFrame

        print('DATAFRAME > ', dataFrame)

        #Consutla MongoDB IDANE (Trae solo IPC de 12-2013)
        gestorDane2013 = self.__getVariablesDane2013(ano)
        cpteC = pd.merge(cpteC, gestorDane2013, on='ano')
        # print("IDANE 2013 - 12 -> ", gestorDane2013)

        #Consutla MongoDB IDANE (trae solo IPC - mes anterior) - cuadrar para cuando sea diciembre
        gestorDane = self.__getVariablesDane(ano, mes)
        cpteC = pd.merge(cpteC, gestorDane, on='ano')
        # print("IDANE IPC M-1 -> ", gestorDane)

        #Consutla MongoDB
        # gestorP097 = self.__getVariablesComercializacion()

        # cpteC = pd.merge(cpteC, gestorP097, on='mercado')

        # cpteC['c15'] = 0

        # cpteC['c8'] = cpteC['c2'] + cpteC['c3'] + cpteC['c4'] + cpteC['c5'] + cpteC['c6'] + cpteC['c7']

        # cpteC['c9'] = (cpteC['c3'] + cpteC['c5'] + cpteC['c7']) / cpteC['c8']

        # cpteC['c16'] = (cpteC['c1'] * (cpteC['c10'] / 100 + cpteC['c9'])) / (1 - (cpteC['c10'] / 100 + cpteC['c9']))

        # cpteC['c20'] = (cpteC['c14'] * cpteC['c10'] / 100) / (1 - cpteC['c10'] / 100) + cpteC['c15']

        # cpteC['c17'] = (cpteC['c1'] * (cpteC['c11'] / 100 + cpteC['c9'])) / (1 - (cpteC['c11'] / 100 + cpteC['c9']))

        # cpteC['c21'] = (cpteC['c14'] * cpteC['c11'] / 100) / (1 - cpteC['c11'] / 100) + cpteC['c15']

        # cpteC['c18'] = (cpteC['c1'] * (cpteC['c12'] / 100 + cpteC['c9'])) / (1 - (cpteC['c12'] / 100 + cpteC['c9']))

        # cpteC['c22'] = (cpteC['c14'] * cpteC['c12'] / 100) / (1 - cpteC['c12'] / 100) + cpteC['c15']

        # cpteC['c19'] = (cpteC['c1'] * (cpteC['c13'] / 100 + cpteC['c9'])) / (1 - (cpteC['c13'] / 100 + cpteC['c9']))

        # cpteC['c23'] = (cpteC['c14'] * cpteC['c13'] / 100) / (1 - cpteC['c13'] / 100) + cpteC['c15']

        # cpteC['nt1'] =  cpteC['c16'] +  cpteC['c20']

        # cpteC['nt2'] =  cpteC['c17'] +  cpteC['c21']

        # cpteC['nt3'] =  cpteC['c18'] +  cpteC['c22']

        # cpteC['nt4'] =  cpteC['c19'] +  cpteC['c23']

        return cpteC
    
    def __getVariablesDane2013(self, ano):
        result = list(self.connMDB.indicesDANE.find({"anio": 2013}, {'meses.diciembre': 1 }))
        key_mes = []
        for x in result:
            for key, value in x['meses'].items():
                key_mes.append(key)

        obj = []

        for m in key_mes:
            result_mes = result[0]['meses'][m]
            ipc = result_mes[len(result_mes)-1]['ipc']
            # ipp = result_mes[len(result_mes)-1]['ipp']
            obj.append([ano,ipc])

        df = pd.DataFrame(obj,columns=['ano','c3'])
        return df
    
    def __getVariablesDane(self, ano, mes):
        MES_ARG = self.meses[int(mes) - 2] # m-1
        result = list(self.connMDB.indicesDANE.find({"anio": ano}, {'meses.' + MES_ARG: 1 }))
        key_mes = []
        for x in result:
            for key, value in x['meses'].items():
                key_mes.append(key)

        obj = []

        for m in key_mes:
            result_mes = result[0]['meses'][m]
            ipc = result_mes[len(result_mes)-1]['ipc']
            # ipp = result_mes[len(result_mes)-1]['ipp']
            obj.append([ano,ipc])

        df = pd.DataFrame(obj,columns=['ano','c4'])
        return df

    def __getVariablesComercializacion(self):
        result = list(self.connMDB.perdidasSTN.find({"anio": 0}))
        key_mercados = []
        for x in result:
            for key, value in x['mercados'].items():
                key_mercados.append(key)

        obj = []

        for m in key_mercados:
            mercado = result[0]['mercados'][m]
            no_mercado = int(m.split('_')[1])
            pr1 = mercado[len(mercado)-1]['pr1']
            pr2 = mercado[len(mercado)-1]['pr2']
            pr3 = mercado[len(mercado)-1]['pr3']
            pr4 = mercado[len(mercado)-1]['pr4']
            obj.append([no_mercado,pr1,pr2,pr3,pr4])

        df = pd.DataFrame(obj,columns=['mercado','c10','c11','c12','c13'])
        return df