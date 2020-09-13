import os
import json


class CpteServiceP097():

    def getData(self, data):
        cpte = []
        cpte.append(
            {
                'ano': data['ano'].tolist()[0],
                'mes': data['mes'].tolist()[0],
                'empresa': data['empresa'].tolist()[0],
                'mercado': data['mercado'].tolist()[0],
                'values': {
                    'CPTEG': [
                        data['c1'].tolist()[0],  # C1 - CG
                    ],
                    'CPTET': [
                        data['c14'].tolist()[0],  # C14 - CT
                    ],
                    'IPRSTN': [
                        data['c9'].tolist()[0],  # C9
                    ],
                    'DEMANDACOMERCIAL': [
                        data['c8'].tolist()[0],  # C8
                        data['c2'].tolist()[0],  # C2
                        data['c3'].tolist()[0],  # C3
                        data['c4'].tolist()[0],  # C4
                        data['c5'].tolist()[0],  # C5
                        data['c6'].tolist()[0],  # C6
                        data['c7'].tolist()[0],  # C7
                    ],
                    'PERDIDASG_NT1': [
                        data['c16'].tolist()[0],  # C16
                    ],
                    'PERDIDAST_NT1': [
                        data['c20'].tolist()[0],  # C20
                        data['c10'].tolist()[0],  # C10
                    ],
                    'PERDIDASG_NT2': [
                        data['c17'].tolist()[0],  # C17
                    ],
                    'PERDIDAST_NT2': [
                        data['c21'].tolist()[0],  # C21
                        data['c11'].tolist()[0],  # C11
                    ],
                    'PERDIDASG_NT3': [
                        data['c18'].tolist()[0],  # C18
                    ],
                    'PERDIDAST_NT3': [
                        data['c22'].tolist()[0],  # C22
                        data['c12'].tolist()[0],  # C12
                    ],
                    'PERDIDASG_NT4': [
                        data['c19'].tolist()[0],  # C19
                    ],
                    'PERDIDAST_NT4': [
                        data['c23'].tolist()[0],  # C23
                        data['c13'].tolist()[0],  # C13
                    ],
                    'CPROG': [
                        data['c15'].tolist()[0],  # C15
                    ],
                    'CPTEP_NT1': [
                        data['nt1'].tolist()[0],  # C24
                    ],
                    'CPTEP_NT2': [
                        data['nt2'].tolist()[0],  # C25
                    ],
                    'CPTEP_NT3': [
                        data['nt3'].tolist()[0],  # C26
                    ],
                    'CPTEP_NT4': [
                        data['nt4'].tolist()[0],  # C27
                    ],
                },
            }
        )
        return cpte
