import os
import json


class CpteServiceDtun():

    def getData(self, data):
        cpte = []
        cpte.append(
            {
                'ano': data['ano'].tolist()[0],
                'mes': data['mes'].tolist()[0],
                'empresa': data['empresa'].tolist()[0],
                'values': {
                    'DTUN_NT1_100': [
                        data['c1'].tolist()[0],  # C1
                    ],
                    'CDI': [
                        data['c2'].tolist()[0],  # C2
                    ],
                    'DTUN_NT1_50': [
                        data['c3'].tolist()[0],  # C3
                    ],
                    'DTUN_NT1_0': [
                        data['c4'].tolist()[0],  # C4
                    ],
                    'DTUN_NT2': [
                        data['c5'].tolist()[0],  # C5
                    ],
                    'DTUN_NT3': [
                        data['c6'].tolist()[0],  # C6
                    ],
                    'DTUN_NT4': [
                        data['c7'].tolist()[0],  # C7
                    ],
                },
            }
        )
        return cpte
