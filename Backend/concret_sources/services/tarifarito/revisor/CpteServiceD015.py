import os
import json


class CpteServiceD015():

    def getData(self, data):
        cpte = []
        for result in data:
            cpte.append({
                'ano': result[23],
                'mes': result[24],
                'empresa': result[25],
                'mercado': result[26], #No aplica para este componente
                'values': {
                    'CARGO_STR_NT1': [
                        result[17],  # C14
                    ],
                    'CARGO_STR_NT2': [
                        result[18],  # C15
                    ],
                    'CARGO_STR_NT3': [
                        result[19],  # C16
                    ],
                    'CARGO_STR_NT4': [
                        result[20],  # C17
                    ],
                    'CD4': [
                        result[8],  # C5
                    ],
                    'PR1': [
                        result[9],  # C6
                    ],
                    'PR2': [
                        result[10],  # C7
                    ],
                    'PR3': [
                        result[11],  # C8
                    ],
                    'PR4': [
                        result[12],  # C9
                    ],
                    'COMPONENTE_DISTRIBUCION_NT1_PROP_OR': [
                        result[21],  # C18
                    ],
                    'COMPONENTE_DISTRIBUCION_NT1_PROP_CLIENTE': [
                        result[22],  # C19
                    ],
                    'COMPONENTE_DISTRIBUCION_NT1_PROP_COMPARTIDA': [
                        result[23],  # C20
                    ],
                    'COMPONENTE_DISTRIBUCION_NT2': [
                        result[24],  # C21
                    ],
                    'COMPONENTE_DISTRIBUCION_NT3': [
                        result[25],  # C22
                    ],
                    'COMPONENTE_DISTRIBUCION_NT4': [
                        result[26],  # C23
                    ],
                    'CDI': [
                        result[4],  # C1
                    ],
                    'CDA': [
                        result[5],  # C2
                    ],
                    'CD2': [
                        result[6],  # C3
                    ],
                    'CD3': [
                        result[7],  # C4
                    ],
                    'P1': [
                        result[13],  # C10
                    ],
                    'Dtcs1': [
                        result[14],  # C11
                    ],
                    'Dtcs2': [
                        result[15],  # C12
                    ],
                    'Dtcs3': [
                        result[16],  # C13
                    ]
                },
            })
        return cpte