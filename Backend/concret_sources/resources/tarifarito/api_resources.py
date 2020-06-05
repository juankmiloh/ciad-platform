from flask import request
from flask_restful import Resource


class apiTarifarito(Resource):
    def get(self):
        return "API TARIFARITO - JUAN CAMILO HERRERA ARDILA | CIAD"