from ....util.ServiceConnection import serviceConnection
import os
import json


class CpteServiceP015():

    def getData(self, data):
        cpte = []
        for result in data:
            cpte.append({
                'ano': result[0],
                'mes': result[1],
                'empresa': result[2],
                'mercado': result[3],
                'values': {
                    'CPTEG': [
                        result[6],  # C1 -CG
                    ],
                    'CPTET': [
                        result[7],  # C14
                    ],
                    'IPRSTN': [
                        result[19],  # C9
                    ],
                    'DEMANDACOMERCIAL': [
                        result[18],  # C8
                        result[8],   # C2
                        result[9],   # C3
                        result[10],  # C4
                        result[11],  # C5
                        result[4],   # C6
                        result[5],   # C7
                    ],
                    'PERDIDASG_NT1': [
                        result[20],  # C16
                    ],
                    'PERDIDAST_NT1': [
                        result[21],  # C20
                        result[15],  # C10
                    ],
                    'PERDIDASG_NT2': [
                        result[22],  # C17
                    ],
                    'PERDIDAST_NT2': [
                        result[23],  # C21
                        result[14],  # C11
                    ],
                    'PERDIDASG_NT3': [
                        result[24],  # C18
                    ],
                    'PERDIDAST_NT3': [
                        result[25],  # C22
                        result[13]   # C12
                    ],
                    'PERDIDASG_NT4': [
                        result[26],  # C19
                    ],
                    'PERDIDAST_NT4': [
                        result[27],  # C23
                        result[12],  # C13
                    ],
                    'CPROG': [
                        result[17],  # C15
                    ],
                    'CPTEP_NT1': [
                        result[28],  # C24
                    ],
                    'CPTEP_NT2': [
                        result[29],  # C25
                    ],
                    'CPTEP_NT3': [
                        result[30],  # C26
                    ],
                    'CPTEP_NT4': [
                        result[31],  # C27
                    ],
                },
            })
        return cpte