from ....util.ServiceConnection import serviceConnection
from ....models.revisor.Componente import Componente
from .CpteServiceG import CpteServiceG
from .CpteServiceT import CpteServiceT
from .CpteServiceP097 import CpteServiceP097
from .CpteServiceP015 import CpteServiceP015
from .CpteServiceD097 import CpteServiceD097
from .CpteServiceD015 import CpteServiceD015
from .CpteServiceC import CpteServiceC


class ComponentService(Componente):
    def __init__(self, componente, ano, mes, empresa, mercado, ntprop):
        super().__init__(componente, ano, mes, empresa, mercado, ntprop)

    def get_model_component(self, data):
        if self._Componente__COMPONENTE == 'G':
            print('-------------------------- COMPONENTE SELECT "G" --------------------')
            cpteService = CpteServiceG()

        if self._Componente__COMPONENTE == 'T':
            print('-------------------------- COMPONENTE SELECT "T" --------------------')
            cpteService = CpteServiceT()
        
        if self._Componente__COMPONENTE == 'P097':
            print('-------------------------- COMPONENTE SELECT "P097" --------------------')
            cpteService = CpteServiceP097()

        if self._Componente__COMPONENTE == 'P015':
            print('-------------------------- COMPONENTE SELECT "P015" --------------------')
            cpteService = CpteServiceP015()
        
        if self._Componente__COMPONENTE == 'D015':
            print('-------------------------- COMPONENTE SELECT "D015" --------------------')
            cpteService = CpteServiceD015()
        
        if self._Componente__COMPONENTE == 'D097':
            print('-------------------------- COMPONENTE SELECT "D097" --------------------')
            cpteService = CpteServiceD097()
        
        if self._Componente__COMPONENTE == 'C':
            print('-------------------------- COMPONENTE SELECT "C" --------------------')
            cpteService = CpteServiceC()
        
        jsonValues = cpteService.getData(data)

        return jsonValues