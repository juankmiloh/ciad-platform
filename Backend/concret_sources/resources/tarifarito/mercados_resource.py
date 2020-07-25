from flask import request
from flask_restful import Resource
from ...models.mercados import MercadosModel


class mercadosTarifarito(Resource):
    def get(self, mercado=0):
        mercadosModel = MercadosModel(mercado)
        self.result = mercadosModel.getMercados()
        return self.result
