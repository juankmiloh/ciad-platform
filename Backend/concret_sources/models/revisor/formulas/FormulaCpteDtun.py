from ....util.ServiceConnection import serviceConnection
import pandas as pd

class FormulaCpteDtun(object):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()

    def merge_perdidas_Dtun(self, dataFrame, mercado):
        #Consulta SQL
        cpteDtun = dataFrame
        # print("DATAFRAME DTUN -> ", cpteDtun)
        
        #Consutla MongoDB perdidas
        gestorValueADD = self.__getValoresADD(mercado)

        cpteDtun = cpteDtun.loc[cpteDtun['ADD'] == gestorValueADD]

        # print("DATAFRAME DTUN - ADD -> ", cpteDtun)

        return cpteDtun

    def __getValoresADD(self, mercado):
        mercado = 'm_' + str(mercado)
        result = list(self.connMDB.infoADD.find({'key':0}, {'mercados.' + mercado: 1}))
        key_mercados = []
        for x in result:
            for key, value in x['mercados'].items():
                key_mercados.append(key)

        obj = []

        for m in key_mercados:
            mercado = result[0]['mercados'][m]
            no_mercado = int(m.split('_')[1])
            add = mercado[len(mercado)-1]['add']

        # print('ADD -> ', add)
        return add
