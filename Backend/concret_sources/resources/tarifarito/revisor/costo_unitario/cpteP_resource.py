from .....config.oracle_connection import OracleConnection
from .....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import os
import json

class rComponentP(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()

    def get(self, anio=0, mes=0, empresa=0, mercado=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__upload_source()
        return self.__getData()

    def __upload_source(self):
        path = os.path.dirname("Sources/tarifarito/")
        file = "/cpteP097.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])

    def __getData(self):
        cpteG = []
        data = self.__execute_query()
        for result in data:
            cpteG.append(
                {
                    # 'ano': result[3],
                    # 'mes': result[4],
                    # 'empresa': result[0],
                    # 'mercado': result[1],
                    'values': {
                        'CPTEG': [
                            result[6], #C1
                        ],
                        'CPTET': [
                            result[7], #C14
                        ],
                        'IPRSTN': [
                            result[17], #C9
                        ],
                        'DEMANDACOMERCIAL': [
                            result[18], #C8
                            result[8],  #C2
                            result[9],  #C3
                            result[10],  #C4
                            result[11],  #C5
                            result[4],  #C6
                            result[5],  #C7
                        ],
                        'PERDIDASG_NT1': [
                            result[20], #C16
                        ],
                        'PERDIDAST_NT1': [
                            result[21], #C20
                            result[15], #C10
                        ],
                        'PERDIDASG_NT2': [
                            result[22], #C17
                        ],
                        'PERDIDAST_NT2': [
                            result[23], #C21
                            result[14], #C11
                        ],
                        'PERDIDASG_NT3': [
                            result[24], #C18
                        ],
                        'PERDIDAST_NT3': [
                            result[25], #C22
                            result[13]   #C12
                        ],
                        'PERDIDASG_NT4': [
                            result[26], #C19
                        ],
                        'PERDIDAST_NT4': [
                            result[27], #C23
                            result[12], #C13
                        ],
                        'CPROG': [
                            result[19], #C15
                        ],
                        'CPTEP_NT1': [
                            result[28], #C24
                        ],
                        'CPTEP_NT2': [
                            result[29], #C25
                        ],
                        'CPTEP_NT3': [
                            result[30], #C26
                        ],
                        'CPTEP_NT4': [
                            result[31], #C27
                        ],
                    },
                }
            )
        return cpteG

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()

        print("________ ANIO ____________")
        print(self.__ANIO_ARG)
        print("____________________________")
        print("________ MES ____________")
        print(self.__PERIODO_ARG)
        print("____________________________")
        print("________ EMPRESA ____________")
        print(self.__EMPRESA_ARG)
        print("____________________________")
        print("________ MERCADO ____________")
        print(self.__MERCADO_ARG)
        print("____________________________")
        print("_________QUERY______________")
        print("SQL:", self.__query)
        print("____________________________")
        pr1 = self.__getVariables()[0]['pr1']
        pr2 = self.__getVariables()[0]['pr2']
        pr3 = self.__getVariables()[0]['pr3']
        pr4 = self.__getVariables()[0]['pr4']
        print('VARIABLE PR1 ----> ')
        print(pr1)
        print('VARIABLE PR1 ----> ')
        cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, PERIODO_ARG=self.__PERIODO_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, MERCADO_ARG=self.__MERCADO_ARG, CAR_T1679_PR1=pr1, CAR_T1679_PR2=pr2, CAR_T1679_PR3=pr3, CAR_T1679_PR4=pr4)
        return cursor

    def post(self):
        req = request.args.get('params')
        print("_________ POST MODEL _____________")
        # print(req)
        print("_________________________________")
        # Insertar datos
        self.connection.componentT.insert_one(
            json.loads(req)
        )
        return req

    def __getVariables(self):
        print("___________ MERCADO _____________")
        print(self.__MERCADO_ARG)
        # Consultar un registro especifico
        mercado = str(self.__MERCADO_ARG)
        result = []
        objeto = {}
        lista = list(self.connection.perdidasSTN.find({'anio':0}, {'mercados.m_'+mercado:1}))
        # print('LISTA ---> ')
        # print(lista)
        # print('LISTA ---> ')
        sizeArray = len(lista[0]['mercados']['m_'+mercado])
        print("___________ SIZEARRAY _____________")
        print(sizeArray)
        objeto['mercado'] = mercado
        for key, value in lista[0]['mercados']['m_'+mercado][sizeArray-1].items():
            objeto[key] = value
        result.append(objeto)
        return result