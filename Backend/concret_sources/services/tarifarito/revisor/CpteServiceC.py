import os
import json


class CpteServiceC():

    def getData(self, data):
        numRows = data.shape[0]
        cpte = []

        for row in range(numRows):
            cpte.append(
                {
                    'ano': data['ano'].tolist()[row],
                    'mes': data['mes'].tolist()[row],
                    'empresa': data['empresa'].tolist()[row],
                    'mercado': data['mercado'].tolist()[row],
                    'values': {
                        'COSTO_BASE_COMERCIALIZACION_ACTUALIZADO': [
                            data['c5'].tolist()[row],  # C5 - CAMBIAR
                        ],
                        'COSTO_BASE_COMERCIALIZACION_AGENTE': [
                            data['c6'].tolist()[row],  # C6
                            data['c1'].tolist()[row],  # C1
                            data['c2'].tolist()[row],  # C2
                            data['c3'].tolist()[row],  # C3
                            data['c4'].tolist()[row],  # C4
                        ],
                        'C*': [
                            data['c43'].tolist()[row],  # C43
                            data['c7'].tolist()[row],  # C7
                            data['c8'].tolist()[row],  # C8
                            data['c9'].tolist()[row],  # C9
                            data['c10'].tolist()[row],  # C10
                            data['c11'].tolist()[row],  # C11
                            data['c12'].tolist()[row],  # C12
                        ],
                        'RC': [
                            data['c27'].tolist()[row],  # C27
                            data['c13'].tolist()[row],  # C13
                            data['c20'].tolist()[row],  # C20
                            data['c22'].tolist()[row],  # C22
                            data['c24'].tolist()[row],  # C24
                            data['c14'].tolist()[row],  # C14
                            data['c21'].tolist()[row],  # C21
                        ],
                        'RCSNE': [
                            data['c18'].tolist()[row],  # C18
                            data['c17'].tolist()[row],  # C17
                            data['c15'].tolist()[row],  # C15
                            data['c16'].tolist()[row],  # C16
                            data['c23'].tolist()[row],  # C23
                            data['c19'].tolist()[row],  # C19
                            data['c25'].tolist()[row],  # C25
                            data['c26'].tolist()[row],  # C26
                        ],
                        'CFE': [
                            data['c42'].tolist()[row],  # C42
                            data['c41'].tolist()[row],  # C41
                            data['c28'].tolist()[row],  # C28
                            data['c29'].tolist()[row],  # C29
                            data['c30'].tolist()[row],  # C30
                            data['c31'].tolist()[row],  # C31
                            data['c39'].tolist()[row],  # C39
                            data['c32'].tolist()[row],  # C32
                            data['c36'].tolist()[row],  # C36
                            data['c34'].tolist()[row],  # C34
                            data['c40'].tolist()[row],  # C40
                            data['c33'].tolist()[row],  # C33
                            data['c37'].tolist()[row],  # C37
                            data['c35'].tolist()[row],  # C35
                            data['c38'].tolist()[row],  # C38
                        ],
                        'CvR': [
                            data['c62'].tolist()[row],  # C62
                            data['c61'].tolist()[row],  # C61
                            data['c59'].tolist()[row],  # C59
                            data['c57'].tolist()[row],  # C57
                            data['c68'].tolist()[row],  # C68
                            data['c69'].tolist()[row],  # C69
                            data['c70'].tolist()[row],  # C70
                            data['c71'].tolist()[row],  # C71
                            data['c58'].tolist()[row],  # C58
                            data['c60'].tolist()[row],  # C60
                        ],
                        'RECONOCIMIENTO_CG_CER_CCD': [
                            data['c63'].tolist()[row],  # C63
                            data['c51'].tolist()[row],  # C51
                            data['c49'].tolist()[row],  # C49
                            data['c50'].tolist()[row],  # C50
                            data['c44'].tolist()[row],  # C44
                            data['c45'].tolist()[row],  # C45
                            data['c47'].tolist()[row],  # C47
                            data['c46'].tolist()[row],  # C46
                            data['c48'].tolist()[row],  # C48
                            data['c54'].tolist()[row],  # C54
                            data['c52'].tolist()[row],  # C52
                            data['c53'].tolist()[row],  # C53
                            data['c55'].tolist()[row],  # C55
                            data['c56'].tolist()[row],  # C56
                        ],
                        '%PART_C*': [
                            data['c65'].tolist()[row],  # C65
                        ],
                        '%PART_CvR': [
                            data['c66'].tolist()[row],  # C66
                        ],
                        '%PART_RECONOCIMIENTO_CG_CER_CCD': [
                            data['c67'].tolist()[row],  # C67
                        ],
                        'Cv': [
                            data['c64'].tolist()[row],  # C64
                        ],
                    },
                }
            )
        return cpte
