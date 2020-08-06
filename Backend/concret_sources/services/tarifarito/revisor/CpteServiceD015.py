from ....util.ServiceConnection import serviceConnection
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
                        result[13],  # C14
                    ],
                    'CARGO_STR_NT2': [
                        result[14],  # C15
                    ],
                    'CARGO_STR_NT3': [
                        result[15],  # C16
                    ],
                    'CARGO_STR_NT4': [
                        result[16],  # C17
                        result[4],  # C5
                        result[5],  # C6
                        result[6],  # C7
                        result[7],  # C8
                        result[8],  # C9
                    ],
                    'CARGO_SDL_NT1_OR': [
                        result[17],  # C18
                    ],
                    'CARGO_SDL_NT1_CLIENTE': [
                        result[18],  # C19
                    ],
                    'CARGO_SDL_NT1_COMPARTIDA': [
                        result[19],  # C20
                    ],
                    'CARGO_SDL_NT2': [
                        result[20],  # C21
                    ],
                    'CARGO_SDL_NT3': [
                        result[21],  # C22
                    ],
                    'CARGO_SDL_NT1_OR': [
                        result[7],  # C23
                        result[0],  # C1
                        result[1],  # C2
                        result[2],  # C3
                        result[3],  # C4
                        result[9],  # C10
                        result[10],  # C11
                        result[11],  # C12
                        result[12],  # C13
                    ],
                },
            })
        return cpte