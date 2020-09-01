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

    def merge_comercializacion(self, dataFrame, result, ano, mes, empresa, modelG, modelT, modelP, modelD, modelR):
        # print('MERCADO > ', mercado)
        # print('EMPRESA > ', empresa)
        # print('COMPONENTE G > ', modelG)
        # print('DATAFRAME MERCADO > ', dataFrame)

        # if result == 'No':
        #     componenteG = Componente("G", ano, mes, empresa, mercado, "No")
        #     componenteT = Componente("T", ano, mes, empresa, mercado, "2")
        #     componenteP015 = Componente("P015", ano, mes, empresa, mercado, "No")
        #     componenteP097 = Componente("P097", ano, mes, empresa, mercado, "No")
        #     componenteD015 = Componente("D015", ano, mes, empresa, mercado, "No")
        #     componenteD097 = Componente("D097", ano, mes, empresa, mercado, "No")
        #     componenteR = Componente("R", ano, mes, empresa, mercado, "No")
            
        #     cpteG = pd.DataFrame(componenteG.get_values_component_SUI())
        #     cpteT = pd.DataFrame(componenteT.get_values_component_SUI())
        #     cpteP015, numrowsCpteP015 = self.get_props_cpte(componenteP015)
        #     cpteP097 = componenteP097.get_values_component_SUI()
        #     cpteP097 = FormulaCpteP097().merge_perdidas_P097(pd.DataFrame(cpteP097, columns=['ano','mes','empresa','mercado','c6','c7','c1','c14','c2','c3','c4','c5']))
        #     cpteD015, numrowsCpteD015 = self.get_props_cpte(componenteD015)
        #     cpteD097 = componenteD097.get_values_component_SUI()
        #     cpteD097 = FormulaCpteD097().merge_perdidas_D097(pd.DataFrame(cpteD097, columns=['ano','mes','empresa','mercado','c5']), ano, mes, empresa)
        #     cpteR = pd.DataFrame(componenteR.get_values_component_SUI())

        #     # --------------------- VALORES CPTE G --------------------- #
        #     modelG = self.get_values_cpteG(cpteG, ano, mes, empresa, mercado)
        #     # --------------------- VALORES CPTE T --------------------- #
        #     modelT = self.get_values_cpteT(cpteT, ano, mes, empresa, mercado)
        #     # --------------------- VALORES CPTE P --------------------- #
        #     modelP = self.get_values_cpteP(numrowsCpteP015, cpteP015, cpteP097, ano, mes, empresa, mercado)
        #     # --------------------- VALORES CPTE D --------------------- #
        #     modelD = self.get_values_cpteD(numrowsCpteD015, cpteD015, cpteD097, ano, mes, empresa, mercado)
        #     # --------------------- VALORES CPTE R --------------------- #
        #     modelR = self.get_values_cpteR(cpteR, ano, mes, empresa, mercado)

        cpteC = dataFrame.loc[dataFrame['mercado'] == result[1]] # Se busca la fila correspondiente al mercado

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

        cpteC['c7'] = 253.7434

        cpteC['c8'] = 38.3961

        cpteC['c9'] = 56.2392

        cpteC['c10'] = 211.2742

        cpteC['c11'] = 0.7642

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

        # sys.stdout = open('log.txt', 'w')
        # print('Write this to file.')

        cpteC.to_csv(r'D:\export_dataframe.csv', mode='a', index = False, header=True)

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

    #  # Función que devuelve los valores del CPTE y ademas permite saber el numero de filas que retorna
    # def get_props_cpte(self, cpte):
    #     df = pd.DataFrame(cpte.get_values_component_SUI())
    #     numRows = df.shape[0]
    #     return df, numRows

    # # Función para obtener valor del cpte 'G'
    # def get_values_cpteG(self, cpteG, ano, mes, empresa, mercado):
    #     #       EMPRESA -                   MERCADO -                  ANIO -                      PERIODO
    #     find = (cpteG[21] == empresa) & (cpteG[22] == mercado) & (cpteG[19] == ano) & (cpteG[20] == mes)
    #     calculado_g = cpteG.loc[find][33].tolist()[0]
    #     modelG = [{ 'value': "G", 'cpte_publicado': 0, 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
    #     return modelG

    # # Función para obtener valor del cpte 'T'
    # def get_values_cpteT(self, cpteT, ano, mes, empresa, mercado):
    #     #       EMPRESA -                   MERCADO -                  ANIO -                      PERIODO -               NTPROP
    #     find = (cpteT[0] == empresa) & (cpteT[1] == mercado) & (cpteT[3] == ano) & (cpteT[4] == mes) & (cpteT[2] == result[4])
    #     calculado_t = cpteT.loc[find][6].tolist()[0]
    #     modelT = [{ 'value': "T", 'cpte_publicado': 0, 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
    #     return modelT

    # # Función para obtener valor del cpte 'P'
    # # Función que permite crear el objeto de acuerdo al NTPROP del result = Datos publicados por la empresa
    # def get_values_cpteP(self, numrowsCpteP015, cpteP015, cpteP097, ano, mes, empresa, mercado):
    #     # print("COMPONENTE | ", numrowsCpteP015, " | CPTEP015 | ", cpteP015, " | CPTEP097 | ", cpteP097, " | RESULT | ", result)
    #     if numrowsCpteP015 > 0:
    #         # --------------------- VALORES CPTE P015 --------------------- #
    #         find = (cpteP015[2] == empresa) & (cpteP015[3] == mercado) & (cpteP015[0] == ano) & (cpteP015[1] == mes)
    #         if result[4].find('1') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP015.loc[find][28].tolist()[0]
    #         if result[4].find('2') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP015.loc[find][29].tolist()[0]
    #         if result[4].find('3') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP015.loc[find][30].tolist()[0]
    #         if result[4].find('4') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP015.loc[find][31].tolist()[0]
    #         modelP = [{ 'value': "P015", 'cpte_publicado': publicado_p, 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P015 publicado:', 'label_calculado': 'Componente P015 calculado:' }]
    #     else:
    #         # --------------------- VALORES CPTE P097 --------------------- #
    #         find = (cpteP097['empresa'] == empresa) & (cpteP097['mercado'] == mercado) & (cpteP097['ano'] == ano) & (cpteP097['mes'] == mes)
    #         if result[4].find('1') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP097['nt1'].tolist()[0]
    #         if result[4].find('2') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP097['nt2'].tolist()[0]
    #         if result[4].find('3') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP097['nt3'].tolist()[0]
    #         if result[4].find('4') != -1:
    #             publicado_p = 0
    #             calculado_p = cpteP097['nt4'].tolist()[0]
    #         modelP = [{ 'value': "P097", 'cpte_publicado': publicado_p, 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P097 publicado:', 'label_calculado': 'Componente P097 calculado:' }]
    #     return modelP
    
    # # Función para obtener valor del cpte 'D'
    # # Función que permite crear el objeto de acuerdo al NTPROP del result = Datos publicados por la empresa
    # def get_values_cpteD(self, numrowsCpteD015, cpteD015, cpteD097, ano, mes, empresa, mercado):
    #     # print("COMPONENTE | ", numrowsCpteD015, " | CPTED015 | ", cpteD015, " | CPTED097 | ", cpteD097, " | RESULT | ", result)
    #     # print("COMPONENTE | ", numrowsCpteD015, " | CPTED015 | ", cpteD015)
    #     if numrowsCpteD015 > 0:
    #         # --------------------- VALORES CPTE D015 --------------------- #
    #         find = (cpteD015[25] == empresa) & (cpteD015[23] == ano) & (cpteD015[24] == mes)
    #         if result[4].find('1-100') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD015.loc[find][17].tolist()[0]
    #         if result[4].find('1-50') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD015.loc[find][18].tolist()[0]
    #         if result[4].find('1-0') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD015.loc[find][19].tolist()[0]
    #         if result[4].find('2') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD015.loc[find][20].tolist()[0]
    #         if result[4].find('3') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD015.loc[find][21].tolist()[0]
    #         if result[4].find('4') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD015.loc[find][7].tolist()[0]
    #         modelD = [{ 'value': "D015", 'cpte_publicado': publicado_d, 'cpte_calculado': calculado_d, 'label_publicado': 'Componente D015 publicado:', 'label_calculado': 'Componente D015 calculado:' }]
    #     else:
    #         print("| CPTED097 -> ", cpteD097)
    #         # --------------------- VALORES CPTE D097 --------------------- #
    #         find = (cpteD097['empresa'] == empresa) & (cpteD097['ano'] == ano) & (cpteD097['mes'] == mes)
    #         if result[4].find('1-100') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD097['c23'].tolist()[0]
    #         if result[4].find('1-50') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD097['c24'].tolist()[0]
    #         if result[4].find('1-0') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD097['c25'].tolist()[0]
    #         if result[4].find('2') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD097['c26'].tolist()[0]
    #         if result[4].find('3') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD097['c27'].tolist()[0]
    #         if result[4].find('4') != -1:
    #             publicado_d = 0
    #             calculado_d = cpteD097['c28'].tolist()[0]
    #         modelD = [{ 'value': "D097", 'cpte_publicado': publicado_d, 'cpte_calculado': calculado_d, 'label_publicado': 'Componente D097 publicado:', 'label_calculado': 'Componente D097 calculado:' }]
    #     return modelD

    # # Función para obtener valor del cpte 'R'
    # def get_values_cpteR(self, cpteR, ano, mes, empresa, mercado):
    #     #       EMPRESA -                   MERCADO -                  ANIO -                      PERIODO
    #     find = (cpteR[0] == empresa) & (cpteR[1] == mercado) & (cpteR[2] == ano) & (cpteR[3] == mes)
    #     calculado_r = cpteR.loc[find][10].tolist()[0]
    #     modelR = [{ 'value': "R", 'cpte_publicado': result[10], 'cpte_calculado': calculado_r, 'label_publicado': 'Componente R publicado:', 'label_calculado': 'Componente R calculado:' }]
    #     return modelR