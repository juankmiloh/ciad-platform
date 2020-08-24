from ....util.ServiceConnection import serviceConnection
import os
import json


class CpteServiceC():

    def getData(self, data):
        cpte = []
        cpte.append(
            {
                'ano': data['ano'].tolist()[0],
                'mes': data['mes'].tolist()[0],
                'empresa': data['empresa'].tolist()[0],
                'mercado': data['mercado'].tolist()[0],
                'ntprop': data['nt_prop'].tolist()[2],
                'values': {
                    'COSTO_BASE_COMERCIALIZACION_ACTUALIZADO': [
                        data['c6'].tolist()[0],  # C5 - CAMBIAR
                    ],
                    'COSTO_BASE_COMERCIALIZACION_AGENTE': [
                        data['c6'].tolist()[0],  # C6
                        # data['c1'].tolist()[0],  # C1
                        # data['c2'].tolist()[0],  # C2
                        # data['c3'].tolist()[0],  # C3
                        # data['c4'].tolist()[0],  # C4
                    ],
                },
            }
        )
        return cpte
