from .....util.ServiceConnection import serviceConnection
from flask import request
from flask_restful import Resource
import os
import json
from .....models.revisor.CpteG import ComponenteG


class rComponentG(Resource):
    def __init__(self):
        connection = serviceConnection()
        self.connMDB = connection.get_connectionMDB()
    
    def get(self, anio=0, mes=0, empresa=0, mercado=0):
        cpteG = ComponenteG(anio, mes, empresa, mercado)
        return cpteG.get_SUI_cpte()

    def post(self):
        req = request.args.get('params')
        self.connMDB.componentG.insert_one(
            json.loads(req)
        )
        return req