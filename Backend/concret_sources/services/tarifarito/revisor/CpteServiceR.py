import os
import json

class CpteServiceR():

    def getData(self, data):
        cpte = []
        for result in data:
            cpte.append(
                {
                    'ANO': result[2],
                    'MES': result[3],
                    'EMPRESA': result[0],
                    'MERCADO': result[1],
                    'values': {
                        'CRS': [
                            result[9], # C5
                            result[5], # C1
                            result[6], # C2
                            result[7], # C3
                            result[4], # C4
                        ],
                        'VENTAS_TOTALES': [
                            result[8], #C6
                        ],
                        'CPTE_RESTRICCIONES': [
                            result[10], #C7
                        ]
                    },
                }
            )
        return cpte