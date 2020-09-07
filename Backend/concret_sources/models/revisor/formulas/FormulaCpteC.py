from ....util.ServiceConnection import serviceConnection
import pandas as pd
from ....models.revisor.Componente import Componente
from ....models.revisor.formulas.FormulaCpteP097 import FormulaCpteP097
from ....models.revisor.formulas.FormulaCpteD097 import FormulaCpteD097
import sys

class FormulaCpteC(object):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def merge_comercializacion(self, dataFrame, ano, mes, empresa, mercado):

        # print('ANO > ', ano)
        # print('MES > ', mes)
        # print('EMPRESA > ', empresa)
        # print('MERCADO > ', mercado)

        cpteC = dataFrame.loc[dataFrame['mercado'] == mercado] # Se busca la fila correspondiente al mercado

        # Consutla MongoDB IDANE (Trae solo IPC de 12-2013)
        gestorDane2013 = self.__getVariablesDane2013(ano)
        cpteC = pd.merge(cpteC, gestorDane2013, on='ano')
        # print("IDANE 2013 - 12 -> ", gestorDane2013)

        #Consutla MongoDB IDANE (trae solo IPC - mes anterior) - cuadrar para cuando sea diciembre
        gestorDane = self.__getVariablesDane(ano, mes)
        cpteC = pd.merge(cpteC, gestorDane, on='ano')
        # print("IDANE IPC M-1 -> ", gestorDane)

        #Consutla MongoDB comercializacion
        gestorC = self.__getVariablesComercializacion(ano, empresa)
        cpteC = pd.merge(cpteC, gestorC, on='empresa')

        # Formula

        cpteC['c5'] = cpteC['c1'] * (1 - cpteC['c2']) * cpteC['c4'] / cpteC['c3']

        cpteC['c17'] = (cpteC['c15'] / 100) + (cpteC['c16'] / 100) + (0.5 * (1 - (cpteC['c15'] / 100) - (cpteC['c16'] / 100))) + 0.05

        cpteC['c26'] = cpteC['c20'] + cpteC['c21'] + cpteC['c22'] + cpteC['c23'] + cpteC['c24'] + cpteC['c25']

        cpteC['c18'] = (1 - cpteC['c17']) / cpteC['c17']

        cpteC['c27'] = ((cpteC['c13'] / 100) * (cpteC['c20'] + cpteC['c22'] + cpteC['c24']) + ((cpteC['c14'] / 100) * cpteC['c21']) + (cpteC['c18'] * cpteC['c23']) + ((cpteC['c19'] / 100) * cpteC['c25'])) / cpteC['c26']

        # cpteC['c39'] = (cpteC['c32'] * ((1 + cpteC['c36'] / 100) ** (cpteC['c34'] + 0.63)) - cpteC['c1']) # TOMAR ESTA - cuadrarla
        cpteC['c39'] = (cpteC['c32'] * (((1 + cpteC['c36']) ** (cpteC['c34'] + 0.63)) - 1)) # PRUEBA CON 524

        # cpteC['c40'] = (cpteC['c33'] * ((1 + cpteC['c37'] / 100) ** (cpteC['c35'])) - cpteC['c1']) # TOMAR ESTA - cuadrarla

        cpteC['c40'] = (cpteC['c33'] * (((1 + cpteC['c37']) ** (cpteC['c35'])) - 1))

        cpteC['c41'] = (cpteC['c39'] - cpteC['c40']) / cpteC['c38']

        cpteC['c42'] = 0.00042 + cpteC['c41']

        cpteC['c12'] = 2.73 / 100 # cambiar por el valor del gestor de datos (MO) crear

        cpteC['c43'] = (cpteC['c7'] + cpteC['c8'] + cpteC['c9'] + cpteC['c10'] + cpteC['c11']) * (cpteC['c12'] + cpteC['c27'] + cpteC['c42'])

        cpteC['c49'] = cpteC['c45'] * cpteC['c47'] / 100 / 12
        
        cpteC['c50'] = cpteC['c46'] * cpteC['c48'] / 100 / 12
        
        cpteC['c51'] = cpteC['c49'] + cpteC['c50']
        
        cpteC['c54'] = cpteC['c52'] + cpteC['c53']

        cpteC['c68'] = cpteC['c70'] * cpteC['c60']

        cpteC['c57'] = cpteC['c68'] + cpteC['c71']

        cpteC['c61'] = 0 # cambiar por el valor del gestor de datos (Beta) crear

        cpteC['c62'] = (((1 - cpteC['c61']) * cpteC['c5'] * cpteC['c59']) + cpteC['c57'] + cpteC['c58']) / cpteC['c60']

        cpteC['c63'] = (cpteC['c51'] + cpteC['c54'] + cpteC['c56']) / cpteC['c55']

        cpteC['c64'] = cpteC['c43'] + cpteC['c63'] + cpteC['c62']
        
        cpteC['c65'] = (cpteC['c43'] / cpteC['c64']) * 100

        cpteC['c66'] = (cpteC['c62'] / cpteC['c64']) * 100
        
        cpteC['c67'] = (cpteC['c63'] / cpteC['c64']) * 100

        # print('DATAFRAME cpte C > ', cpteC)

        # cpteC.to_csv(r'D:\export_dataframe.csv', mode='a', index = False, header=True) # LINEA PARA EXPORTAR DATAFRAME A EXCEL CSV

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

    def __getVariablesComercializacion(self, ano, empresa):
        result = list(self.connMDB.infoComercial.find({"anio": ano}, {'empresas.e_'+ str(empresa): 1 }))
        key_empresa = []
        for x in result:
            for key, value in x['empresas'].items():
                key_empresa.append(key)

        obj = []

        for e in key_empresa:
            empresa = result[0]['empresas'][e]
            no_empresa = int(e.split('_')[1])
            factorP = empresa[len(empresa)-1]['factorP']
            rcnu = empresa[len(empresa)-1]['rcnu']
            ccreg = empresa[len(empresa)-1]['ccreg']
            csspd = empresa[len(empresa)-1]['csspd']
            # rcreg = empresa[len(empresa)-1]['rcreg']
            # rsspd = empresa[len(empresa)-1]['rsspd']
            # obj.append([no_empresa,factorP,rcnu,ccreg,csspd,rcreg,rsspd])
            obj.append([no_empresa,factorP,rcnu,ccreg,csspd])

        df = pd.DataFrame(obj,columns=['empresa','c2','c19','c45','c46'])
        return df