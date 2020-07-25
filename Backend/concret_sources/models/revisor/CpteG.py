from ...util.ServiceConnection import serviceConnection
import os
import json

class ComponenteG():

    def __init__(self, anio, mes, empresa, mercado):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        connection = serviceConnection()
        self.cursorSUI = connection.get_connectionSUI()
        self.connMDB = connection.get_connectionMDB()

    def get_SUI_cpte(self):
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteG.json"
        source = json.load(open(path + file))
        self.__query = ''.join(source["query"])

    def __getData(self):
        cpteG = []
        data = self.__execute_query()
        for result in data:
            cpteG.append(
                {
                    'ANO': result[19],
                    'MES': result[20],
                    'values': {
                        'DCR': [
                            result[24], # C16
                            result[0],  # C12
                            result[9],  # C13
                            result[1],  # C14
                            result[10], # C15
                        ],
                        'Qc': [
                            result[25], #C17
                        ],
                        'Pc': [
                            result[26], #C22
                            result[4],  #C1
                            result[2],  #C2
                            result[5],  #C3
                            result[6],  #C4
                            result[3],  #C5
                            result[11], #C6
                        ],
                        'Qb': [
                            result[27], #C18
                        ],
                        'Pb': [
                            result[28], #C23
                            result[7],  #C7
                            result[8],  #C8
                        ],
                        'Qagd': [
                            result[29], #C21
                            result[12], #C19
                            result[13], #C20
                        ],
                        'McAplicado': [
                            result[30], #C11
                            result[23], #C9
                            result[18], #C10
                        ],
                        'FAJ': [
                            result[14], #C24
                        ],
                        'ALFA': [
                            result[15], #C25
                        ],
                        'GTransitorio': [
                            result[16], #C26
                        ],
                        'GContratos': [
                            result[31], #C29
                        ],
                        'GBolsa': [
                            result[32], #C30
                        ],
                        'CFNC': [
                            result[17], #C27
                        ],
                        'CGeneracion': [
                            result[33]  #C28
                        ],
                    },
                }
            )
        return cpteG

    def __execute_query(self):
        self.cursorSUI.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG)
        return self.cursorSUI