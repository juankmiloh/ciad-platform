import os
import json


class CpteServiceD097():

    def getData(self, data):
        cpte = []
        cpte.append(
            {
                'ano': data['ano'].tolist()[0],
                'mes': data['mes'].tolist()[0],
                'empresa': data['empresa'].tolist()[0],
                'mercado': data['mercado'].tolist()[0],
                'values': {
                    'CARGO_STR_NT1': [
                        data['c13'].tolist()[0],  # C13
                    ],
                    'CARGO_STR_NT2': [
                        data['c14'].tolist()[0],  # C14
                    ],
                    'CARGO_STR_NT3': [
                        data['c15'].tolist()[0],  # C15
                    ],
                    'CARGO_STR_NT4': [
                        data['c16'].tolist()[0],  # C16
                    ],
                    'CD4': [
                        data['c5'].tolist()[0],  # C5
                    ],
                    'PR1': [
                        data['c8'].tolist()[0],  # C8
                    ],
                    'PR2': [
                        data['c9'].tolist()[0],  # C9
                    ],
                    'PR3': [
                        data['c10'].tolist()[0],  # C10
                    ],
                    'PR4': [
                        data['c11'].tolist()[0],  # C11
                    ],
                    'PR1-2': [
                        data['c12'].tolist()[0],  # C12
                    ],
                    'CARGO_SDL_NT1_NT2': [
                        data['c17'].tolist()[0],  # C17
                    ],
                    'CARGO_SDL_NT1_OR': [
                        data['c18'].tolist()[0],  # C18
                    ],
                    'CARGO_SDL_NT1_CLIENTE': [
                        data['c19'].tolist()[0],  # C19
                    ],
                    'CARGO_SDL_NT1_COMPARTIDA': [
                        data['c20'].tolist()[0],  # C20
                    ],
                    'CARGO_SDL_NT2': [
                        data['c21'].tolist()[0],  # C21
                    ],
                    'CARGO_SDL_NT3': [
                        data['c22'].tolist()[0],  # C22
                    ],
                    'IPP_DIC_2017': [
                        data['c6'].tolist()[0],  # C6
                    ],
                    'IPP_M_1': [
                        data['c7'].tolist()[0],  # C7
                    ],
                    'CDI': [
                        data['c1'].tolist()[0],  # C1
                    ],
                    'CDM': [
                        data['c2'].tolist()[0],  # C2
                    ],
                    'CD2': [
                        data['c3'].tolist()[0],  # C3
                    ],
                    'CD3': [
                        data['c4'].tolist()[0],  # C4
                    ],
                    'COMPONENTE_NT1_OR': [
                        data['c23'].tolist()[0],  # C23
                    ],
                    'COMPONENTE_NT1_CLIENTE': [
                        data['c24'].tolist()[0],  # C24
                    ],
                    'COMPONENTE_NT1_COMPARTIDA': [
                        data['c25'].tolist()[0],  # C25
                    ],
                    'COMPONENTE_NT2': [
                        data['c26'].tolist()[0],  # C26
                    ],
                    'COMPONENTE_NT3': [
                        data['c27'].tolist()[0],  # C27
                    ],
                    'COMPONENTE_NT4': [
                        data['c28'].tolist()[0],  # C28
                    ],
                },
            }
        )
        return cpte
