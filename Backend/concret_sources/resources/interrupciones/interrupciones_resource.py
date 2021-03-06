import datetime
import csv
import os
import json

from flask import send_from_directory
from flask import send_file  # descargar archivos

from flask import request
from flask_restful import Resource
from ...config.oracle_connection import OracleConnection


class dataInterrupcion(Resource):
    def get(self, anio=0, mes=0, empresa=0, causa=0):
        now = datetime.datetime.now()
        self.__ANIO_ARG = now.year if anio == 0 else anio
        # self.__ANIO_ARG = 2018
        self.__MES_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__CAUSA = causa if causa != 0 else 0
        self._PNEXC_ARG = 0
        self._NPNEXC_ARG = 0
        self._REMER_ARG = 0
        self._STNSTR_ARG = 0
        self._SEGCIU_ARG = 0
        self._FNIVEL1_ARG = 0
        self._CASTNAT_ARG = 0
        self._TERR_ARG = 0
        self._CALZESP_ARG = 0
        self._TSUBEST_ARG = 0
        self._INFRA_ARG = 0
        self._SUMI_ARG = 0
        self._EXP_ARG = 0
        if self.__CAUSA == 0:
            # condicional ALLCAUSAS TRUE
            self._PNEXC_ARG = 16
            self._NPNEXC_ARG = 18
            self._REMER_ARG = 20
            self._STNSTR_ARG = 22
            self._SEGCIU_ARG = 24
            self._FNIVEL1_ARG = 26
            self._CASTNAT_ARG = 28
            self._TERR_ARG = 30
            self._CALZESP_ARG = 32
            self._TSUBEST_ARG = 34
            self._INFRA_ARG = 36
            self._SUMI_ARG = 38
            self._EXP_ARG = 40
        else:
            # condicional ALLCAUSAS FALSE
            self.__sendCause(self.__CAUSA)
        self.__upload_source()
        return self.__getData()

    def __sendCause(self, causa):
        if causa == 16:
            self._PNEXC_ARG = 16
        if causa == 18:
            self._NPNEXC_ARG = 18
        if causa == 20:
            self._REMER_ARG = 20
        if causa == 22:
            self._STNSTR_ARG = 22
        if causa == 24:
            self._SEGCIU_ARG = 24
        if causa == 26:
            self._FNIVEL1_ARG = 26
        if causa == 28:
            self._CASTNAT_ARG = 28
        if causa == 30:
            self._TERR_ARG = 30
        if causa == 32:
            self._CALZESP_ARG = 32
        if causa == 34:
            self._TSUBEST_ARG = 34
        if causa == 36:
            self._INFRA_ARG = 36
        if causa == 38:
            self._SUMI_ARG = 38
        if causa == 40:
            self._EXP_ARG = 40

    def __upload_source(self):
        path = os.path.dirname("Sources/interrupciones/")
        file = "/interrupciones.json"
        source = json.load(open(path + file))
        self.__set_source(source)

    def __set_source(self, source):
        self.__name = source["name"]  # nombre del json
        # query que se quiere hacer y se concatena porque es un string
        self.__query = ''.join(source["query"])
        # print(self.__query)

    def __getData(self):
        interrupciones = []
        data = self.__execute_query()
        for result in data:
            interrupciones.append(
                {
                    'nom_empresa': result[0],
                    'centro_poblado': result[1],
                    'longitude': result[2],
                    'latitude': result[3],
                    'cod_dane': result[4],
                    'cod_empresa': result[5],
                    'ano': result[6],
                    'mes': result[7],
                    'pnexc': result[8],
                    'npnexc': result[9],
                    'remer': result[10],
                    'stnstr': result[11],
                    'segciu': result[12],
                    'fnivel1': result[13],
                    'castnat': result[14],
                    'terr': result[15],
                    'calzesp': result[16],
                    'tsubest': result[17],
                    'infra': result[18],
                    'sumi': result[19],
                    'exp': result[20],
                    'total': result[21],
                    'chrome': 1 # Esto se coloca para que renderice el mapa en chrome
                }
            )
        return self.__getCSV(interrupciones)

    def __getCSV(self, arrayInterrupciones):
        with open('file_interrupciones.csv', 'w', newline='') as csvfile:
            fieldnames = ['nom_empresa', 'centro_poblado', 'longitude', 'latitude', 'cod_dane', 'cod_empresa', 'ano', 'mes', 'pnexc', 'npnexc',
                          'remer', 'stnstr', 'segciu', 'fnivel1',  'castnat', 'terr', 'calzesp', 'tsubest', 'infra', 'sumi', 'exp', 'total', 'chrome']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arrayInterrupciones)
        return send_file('file_interrupciones.csv', as_attachment=True)

    def __execute_query(self):
        oracleConnection = OracleConnection()
        connection = oracleConnection.get_connection()
        cursor = connection.cursor()
        print("________ANIO________________")
        print(self.__ANIO_ARG)
        print("____________________________")
        print("________MES_________________")
        print(self.__MES_ARG)
        print("____________________________")
        print("________EMPRESA_____________")
        print(self.__EMPRESA_ARG)
        print("____________________________")
        print("____________________________")
        print("__________CAUSA____________")
        print(self.__CAUSA)
        print("____________________________")
        print("____________________________")
        print("SQL:", self.__query)
        print("____________________________")
        cursor.execute(self.__query, ANIO_ARG=self.__ANIO_ARG, MES_ARG=self.__MES_ARG, EMPRESA_ARG=self.__EMPRESA_ARG, PNEXC_ARG=self._PNEXC_ARG, NPNEXC_ARG=self._NPNEXC_ARG, REMER_ARG=self._REMER_ARG, STNSTR_ARG=self._STNSTR_ARG, SEGCIU_ARG=self._SEGCIU_ARG,
                       FNIVEL1_ARG=self._FNIVEL1_ARG, CASTNAT_ARG=self._CASTNAT_ARG, TERR_ARG=self._TERR_ARG, CALZESP_ARG=self._CALZESP_ARG, TSUBEST_ARG=self._TSUBEST_ARG, INFRA_ARG=self._INFRA_ARG, SUMI_ARG=self._SUMI_ARG, PEXP_ARG=self._EXP_ARG)
        return cursor
