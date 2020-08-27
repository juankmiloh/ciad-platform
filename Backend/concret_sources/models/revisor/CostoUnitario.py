from ...util.ServiceConnection import serviceConnection
import os
import json
import pandas as pd


class CostoUnitario():

    # Se inicializan las variables de la clase (recibidas desde el ENDPOINT)
    def __init__(self, anio, mes, empresa, mercado, ntprop):
        self.__ANIO_ARG = anio
        self.__PERIODO_ARG = mes
        self.__EMPRESA_ARG = empresa
        self.__MERCADO_ARG = mercado
        self.__NTPROP_ARG = ntprop
        connection = serviceConnection()
        self.cursor = connection.get_connectionSUI()

    # Se obtienen los valores publicados por la empresa en FT7
    def getCostoUnitario(self):
        self.upload_source()
        return self.getData()

    def upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/costo_unitario.json"
        source = json.load(open(path + file))
        self.__query = ''.join(source["query"])

    def getData(self):
        data = self.execute_query()
        return data

    def execute_query(self):
        self.cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        return self.cursor

    # Función que devuelve los valores del CPTE y ademas permite saber el numero de filas que retorna
    def get_props_cpte(self, cpte):
        df = pd.DataFrame(cpte.get_values_component_SUI())
        numRows = df.shape[0]
        return df, numRows

    # Función para obtener valor del cpte 'G'
    def get_values_cpteG(self, cpteG, result):
        #       EMPRESA -                   MERCADO -                  ANIO -                      PERIODO
        find = (cpteG[21] == result[12]) & (cpteG[22] == result[1]) & (cpteG[19] == result[13]) & (cpteG[20] == result[14])
        calculado_g = cpteG.loc[find][33].tolist()[0]
        modelG = [{ 'value': "G", 'cpte_publicado': result[5], 'cpte_calculado': calculado_g, 'label_publicado': 'Componente G publicado:', 'label_calculado': 'Componente G calculado:' }]
        return modelG

    # Función para obtener valor del cpte 'T'
    def get_values_cpteT(self, cpteT, result):
        #       EMPRESA -                   MERCADO -                  ANIO -                      PERIODO -               NTPROP
        find = (cpteT[0] == result[12]) & (cpteT[1] == result[1]) & (cpteT[3] == result[13]) & (cpteT[4] == result[14]) & (cpteT[2] == result[4])
        calculado_t = cpteT.loc[find][6].tolist()[0]
        modelT = [{ 'value': "T", 'cpte_publicado': result[6], 'cpte_calculado': calculado_t, 'label_publicado': 'Componente T empresa:', 'label_calculado': 'Componente T LAC:' }]
        return modelT

    # Función para obtener valor del cpte 'P'
    # Función que permite crear el objeto de acuerdo al NTPROP del result = Datos publicados por la empresa
    def get_values_cpteP(self, numrowsCpteP015, cpteP015, cpteP097, result):
        # print("COMPONENTE | ", numrowsCpteP015, " | CPTEP015 | ", cpteP015, " | CPTEP097 | ", cpteP097, " | RESULT | ", result)
        if numrowsCpteP015 > 0:
            # --------------------- VALORES CPTE P015 --------------------- #
            find = (cpteP015[2] == result[12]) & (cpteP015[3] == result[1]) & (cpteP015[0] == result[13]) & (cpteP015[1] == result[14])
            if result[4].find('1') != -1:
                publicado_p = result[7]
                calculado_p = cpteP015.loc[find][28].tolist()[0]
            if result[4].find('2') != -1:
                publicado_p = result[7]
                calculado_p = cpteP015.loc[find][29].tolist()[0]
            if result[4].find('3') != -1:
                publicado_p = result[7]
                calculado_p = cpteP015.loc[find][30].tolist()[0]
            if result[4].find('4') != -1:
                publicado_p = result[7]
                calculado_p = cpteP015.loc[find][31].tolist()[0]
            modelP = [{ 'value': "P015", 'cpte_publicado': publicado_p, 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P015 publicado:', 'label_calculado': 'Componente P015 calculado:' }]
        else:
            # --------------------- VALORES CPTE P097 --------------------- #
            find = (cpteP097['empresa'] == result[12]) & (cpteP097['mercado'] == result[1]) & (cpteP097['ano'] == result[13]) & (cpteP097['mes'] == result[14])
            if result[4].find('1') != -1:
                publicado_p = result[7]
                calculado_p = cpteP097['nt1'].tolist()[0]
            if result[4].find('2') != -1:
                publicado_p = result[7]
                calculado_p = cpteP097['nt2'].tolist()[0]
            if result[4].find('3') != -1:
                publicado_p = result[7]
                calculado_p = cpteP097['nt3'].tolist()[0]
            if result[4].find('4') != -1:
                publicado_p = result[7]
                calculado_p = cpteP097['nt4'].tolist()[0]
            modelP = [{ 'value': "P097", 'cpte_publicado': publicado_p, 'cpte_calculado': calculado_p, 'label_publicado': 'Componente P097 publicado:', 'label_calculado': 'Componente P097 calculado:' }]
        return modelP
    
    # Función para obtener valor del cpte 'D'
    # Función que permite crear el objeto de acuerdo al NTPROP del result = Datos publicados por la empresa
    def get_values_cpteD(self, numrowsCpteD015, cpteD015, cpteD097, result):
        # print("COMPONENTE | ", numrowsCpteD015, " | CPTED015 | ", cpteD015, " | CPTED097 | ", cpteD097, " | RESULT | ", result)
        # print("COMPONENTE | ", numrowsCpteD015, " | CPTED015 | ", cpteD015)
        if numrowsCpteD015 > 0:
            # --------------------- VALORES CPTE D015 --------------------- #
            find = (cpteD015[25] == result[12]) & (cpteD015[23] == result[13]) & (cpteD015[24] == result[14])
            if result[4].find('1-100') != -1:
                publicado_d = result[8]
                calculado_d = cpteD015.loc[find][17].tolist()[0]
            if result[4].find('1-50') != -1:
                publicado_d = result[8]
                calculado_d = cpteD015.loc[find][18].tolist()[0]
            if result[4].find('1-0') != -1:
                publicado_d = result[8]
                calculado_d = cpteD015.loc[find][19].tolist()[0]
            if result[4].find('2') != -1:
                publicado_d = result[8]
                calculado_d = cpteD015.loc[find][20].tolist()[0]
            if result[4].find('3') != -1:
                publicado_d = result[8]
                calculado_d = cpteD015.loc[find][21].tolist()[0]
            if result[4].find('4') != -1:
                publicado_d = result[8]
                calculado_d = cpteD015.loc[find][7].tolist()[0]
            modelD = [{ 'value': "D015", 'cpte_publicado': publicado_d, 'cpte_calculado': calculado_d, 'label_publicado': 'Componente D015 publicado:', 'label_calculado': 'Componente D015 calculado:' }]
        else:
            print("| CPTED097 -> ", cpteD097)
            # --------------------- VALORES CPTE D097 --------------------- #
            find = (cpteD097['empresa'] == result[12]) & (cpteD097['ano'] == result[13]) & (cpteD097['mes'] == result[14])
            if result[4].find('1-100') != -1:
                publicado_d = result[8]
                calculado_d = cpteD097['c23'].tolist()[0]
            if result[4].find('1-50') != -1:
                publicado_d = result[8]
                calculado_d = cpteD097['c24'].tolist()[0]
            if result[4].find('1-0') != -1:
                publicado_d = result[8]
                calculado_d = cpteD097['c25'].tolist()[0]
            if result[4].find('2') != -1:
                publicado_d = result[8]
                calculado_d = cpteD097['c26'].tolist()[0]
            if result[4].find('3') != -1:
                publicado_d = result[8]
                calculado_d = cpteD097['c27'].tolist()[0]
            if result[4].find('4') != -1:
                publicado_d = result[8]
                calculado_d = cpteD097['c28'].tolist()[0]
            modelD = [{ 'value': "D097", 'cpte_publicado': publicado_d, 'cpte_calculado': calculado_d, 'label_publicado': 'Componente D097 publicado:', 'label_calculado': 'Componente D097 calculado:' }]
        return modelD

    # Función para obtener valor del cpte 'C'
    def get_values_cpteC(self, cpteC, result):
        #       EMPRESA -                              MERCADO -                         ANIO -                      PERIODO -               NTPROP
        find = (cpteC['empresa'] == result[12]) & (cpteC['mercado'] == result[1]) & (cpteC['ano'] == result[13]) & (cpteC['mes'] == result[14]) & (cpteC['nt_prop'] == result[4])
        calculado_c = cpteC['c64'].tolist()[0]
        modelC = [{ 'value': "C", 'cpte_publicado': result[9], 'cpte_calculado': calculado_c, 'label_publicado': 'Componente C publicado:', 'label_calculado': 'Componente C calculado:' }]
        return modelC

    # Función para obtener valor del cpte 'R'
    def get_values_cpteR(self, cpteR, result):
        #       EMPRESA -                   MERCADO -                  ANIO -                      PERIODO
        find = (cpteR[0] == result[12]) & (cpteR[1] == result[1]) & (cpteR[2] == result[13]) & (cpteR[3] == result[14])
        calculado_r = cpteR.loc[find][10].tolist()[0]
        modelR = [{ 'value': "R", 'cpte_publicado': result[10], 'cpte_calculado': calculado_r, 'label_publicado': 'Componente R publicado:', 'label_calculado': 'Componente R calculado:' }]
        return modelR