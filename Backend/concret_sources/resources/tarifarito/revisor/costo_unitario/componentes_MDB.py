from .....config.mongodb_connection import MongoConnection
from flask import request
from flask_restful import Resource
import json


class rComponentesMDB(Resource):
    def __init__(self):
        mongodb_connection = MongoConnection()
        self.connection = mongodb_connection.get_connection()

    def get(self, anio=0, mes=0, empresa=0, mercado=0, componente="", ntprop=""):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__MES_ARG = mes if mes != 0 else 0
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__CPTE_ARG = componente if componente != "" else "TODOS"
        self.__NTPROP_ARG = ntprop if ntprop != "" else "TODOS"
        return self.__getData()

    def __getData(self):
        data = self.__execute_query()
        return data

    def __execute_query(self):
        print("GET ANIO -> ", self.__ANIO_ARG)
        print("GET MES -> ", self.__MES_ARG)
        print("GET EMPRESA -> ", self.__EMPRESA_ARG)
        print("GET MERCADO -> ", self.__MERCADO_ARG)
        print("GET CPTE -> ", self.__CPTE_ARG)
        print("GET NTPROP -> ", self.__NTPROP_ARG)
        if self.__CPTE_ARG == "TODOS" and self.__NTPROP_ARG == "TODOS":
            mydoc = self.connection.componentes.aggregate( [
                { "$match" : {'ano':self.__ANIO_ARG, 'mes':self.__MES_ARG, 'cod_empresa': self.__EMPRESA_ARG, 'cod_mercado': self.__MERCADO_ARG} },
                { "$group" : {
                    "_id": {"nt_prop": "$nt_prop", "componente": "$componente"},
                    "usuario": { "$last": "$usuario" },
                    "ano": { "$last": "$ano" },
                    "mes": { "$last": "$mes" },
                    "cod_empresa": { "$last": "$cod_empresa" },
                    "nom_empresa": { "$last": "$nom_empresa" },
                    "cod_mercado": { "$last": "$cod_mercado" },
                    "nom_mercado": { "$last": "$nom_mercado" },
                    "componente": { "$last": "$componente" },
                    "nt_prop": { "$last": "$nt_prop" },
                    "novedad": { "$last": "$novedad" },
                    "fecha_modif": { "$last": "$fecha_modif" },
                    "estado": { "$last": "$estado" } } }
                ] );
            mydoc = list(mydoc)
        else:
            # TRAEMOS TODO EL HISTORICO DEL COMPONENTE GURADADO
            mydoc = []
            result = self.connection.componentes.find({'ano':self.__ANIO_ARG, 'mes':self.__MES_ARG, 'cod_empresa': self.__EMPRESA_ARG, 'cod_mercado': self.__MERCADO_ARG, 'componente': self.__CPTE_ARG, 'nt_prop': self.__NTPROP_ARG}).sort([("fecha_modif", -1)])
            for item in result:
                mydoc.append(
                    {
                        'usuario': item['usuario'],
                        "ano": item['ano'],
                        "mes": item['mes'],
                        "cod_empresa": item['cod_empresa'],
                        "nom_empresa": item['nom_empresa'],
                        "cod_mercado": item['cod_mercado'],
                        "nom_mercado": item['nom_mercado'],
                        "componente": item['componente'],
                        "nt_prop": item['nt_prop'],
                        "novedad": item['novedad'],
                        "fecha_modif": item['fecha_modif'],
                        "estado": item['estado'],
                        "componentes": item['componentes'],
                        "values": item['values']
                    }
                )
        return mydoc

    def post(self):
        req = request.args.get('params')
        print("_________ POST MODEL _____________")
        print(req)
        print("_________________________________")
        # Insertar datos
        self.connection.nivelTolerancia.insert_one(
            json.loads(req)
        )
        return req

    def put(self, anio=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        req_model = request.args['params']
        req_mes = request.args.get('mes')
        print("_________ PUT MODEL _____________")
        print(req_model)
        print("_________________________________")
        # Modificar datos
        self.connection.nivelTolerancia.update_one(
            {"anio": self.__ANIO_ARG},
            {"$push": {"meses."+req_mes: {"$each": [json.loads(req_model)]}}}
        )
        return req_model

    def delete(self, anio=0):
        self.__ANIO_ARG = anio if anio != 0 else 0
        print("_________ DELETE ANIO ___________")
        print(self.__ANIO_ARG)
        print("_________________________________")
        # Borrar documento
        self.connection.nivelTolerancia.delete_one(
            {"anio": self.__ANIO_ARG}
        )
        return self.__ANIO_ARG
