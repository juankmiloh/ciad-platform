from flask import request
from flask_restful import Resource


class apiHome(Resource):
    def get(self):
        return "API HOME - JUAN CAMILO HERRERA ARDILA | CIAD"