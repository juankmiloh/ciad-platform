from ....util.ServiceConnection import serviceConnection
import pandas as pd

class FormulaCpteD097(object):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    def merge_perdidas_D097(self, dataFrame, ano, mes, empresa):
        #Consulta SQL
        cpteD097 = dataFrame

        #Consutla MongoDB perdidas
        gestorPerdidas = self.__getVariablesPerdidas()

        cpteD097 = pd.merge(cpteD097, gestorPerdidas, on='mercado')

        #Consutla MongoDB distribucion
        gestorD = self.__getVariablesDistribucion(ano, empresa)

        cpteD097 = pd.merge(cpteD097, gestorD, on='empresa')
        
        #Consutla MongoDB IDANE (trae solo IPP)
        gestorDane = self.__getVariablesDane(ano, mes)

        cpteD097 = pd.merge(cpteD097, gestorDane, on='mes')
        
        #Consutla MongoDB IDANE (Trae solo IPC de 12-2007)
        gestorDane2007 = self.__getVariablesDane2007(ano)

        cpteD097 = pd.merge(cpteD097, gestorDane2007, on='ano')

        cpteD097['c13'] = cpteD097['c5'] / (1 - cpteD097['c8'] / 100)
        cpteD097['c14'] = cpteD097['c5'] / (1 - cpteD097['c9'] / 100)
        cpteD097['c15'] = cpteD097['c5'] / (1 - cpteD097['c10'] / 100)
        cpteD097['c16'] = cpteD097['c5'] / (1 - cpteD097['c11'] / 100)

        cpteD097['c17'] = (cpteD097['c3'] * cpteD097['c7'] / cpteD097['c6']) / (1 - cpteD097['c12'] / 100)
        cpteD097['c18'] = (cpteD097['c1'] + cpteD097['c2']) * (cpteD097['c7'] / cpteD097['c6'])
        cpteD097['c19'] = cpteD097['c2'] * (cpteD097['c7'] / cpteD097['c6'])
        cpteD097['c20'] = (cpteD097['c1'] / 2 *(cpteD097['c7'] / cpteD097['c6'])) + (cpteD097['c2'] * (cpteD097['c7'] / cpteD097['c6']))
        cpteD097['c21'] = cpteD097['c3'] * (cpteD097['c7'] / cpteD097['c6'])
        cpteD097['c22'] = cpteD097['c4'] * (cpteD097['c7'] / cpteD097['c6'])

        cpteD097['c23'] = cpteD097['c18'] + cpteD097['c17'] + cpteD097['c13'] 
        cpteD097['c24'] = cpteD097['c19'] + cpteD097['c17'] + cpteD097['c13'] 
        cpteD097['c25'] = cpteD097['c20'] + cpteD097['c17'] + cpteD097['c13'] 
        cpteD097['c26'] = cpteD097['c21'] + cpteD097['c14']
        cpteD097['c27'] = cpteD097['c22'] + cpteD097['c15']
        cpteD097['c28'] = cpteD097['c16']

        # print("DATAFRAME D097 - COMPLETO -> ", cpteD097)

        return cpteD097

    def __getVariablesPerdidas(self):
        result = list(self.connMDB.perdidasSTN.find({"anio": 0}))
        key_mercados = []
        for x in result:
            for key, value in x['mercados'].items():
                key_mercados.append(key)

        obj = []

        for m in key_mercados:
            mercado = result[0]['mercados'][m]
            no_mercado = int(m.split('_')[1])
            pr12 = mercado[len(mercado)-1]['pr1_2']
            pr1 = mercado[len(mercado)-1]['pr1']
            pr2 = mercado[len(mercado)-1]['pr2']
            pr3 = mercado[len(mercado)-1]['pr3']
            pr4 = mercado[len(mercado)-1]['pr4']
            obj.append([no_mercado,pr12,pr1,pr2,pr3,pr4])

        df = pd.DataFrame(obj,columns=['mercado','c12','c8','c9','c10','c11'])
        # print('DF -> ', df)
        return df

    def __getVariablesDistribucion(self, ano, empresa):
        result = list(self.connMDB.infoD097Res.find({"anio": ano}, {'empresas.e_'+ str(empresa): 1 }))
        key_empresa = []
        for x in result:
            for key, value in x['empresas'].items():
                key_empresa.append(key)

        obj = []

        for e in key_empresa:
            empresa = result[0]['empresas'][e]
            no_empresa = int(e.split('_')[1])
            cdi = empresa[len(empresa)-1]['cdi']
            cdm = empresa[len(empresa)-1]['cdm']
            cd2 = empresa[len(empresa)-1]['cd2']
            cd3 = empresa[len(empresa)-1]['cd3']
            obj.append([no_empresa,cdi,cdm,cd2,cd3])

        df = pd.DataFrame(obj,columns=['empresa','c1','c2','c3','c4'])
        return df
    
    def __getVariablesDane(self, ano, mes):
        MES_ARG = self.meses[int(mes) - 1]
        result = list(self.connMDB.indicesDANE.find({"anio": ano}, {'meses.' + MES_ARG: 1 }))
        key_mes = []
        for x in result:
            for key, value in x['meses'].items():
                key_mes.append(key)

        obj = []

        for m in key_mes:
            result_mes = result[0]['meses'][m]
            # ipc = result_mes[len(result_mes)-1]['ipc']
            ipp = result_mes[len(result_mes)-1]['ipp']
            obj.append([mes,ipp])

        df = pd.DataFrame(obj,columns=['mes','c7'])
        return df
    
    def __getVariablesDane2007(self, ano):
        result = list(self.connMDB.indicesDANE.find({"anio": 2007}, {'meses.diciembre': 1 }))
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

        df = pd.DataFrame(obj,columns=['ano','c6'])
        return df