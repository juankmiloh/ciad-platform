from concret_sources.resources.home_resource import apiHome

from concret_sources.resources.pqrs.pqrs_resource import PqrsRsource
from concret_sources.resources.pqrs.empresas_resource import EmpresasRsource
from concret_sources.resources.pqrs.causas_resource import CausasRsource
from concret_sources.resources.pqrs.pqrs_causas_resource import PqrsCausasRsource
from concret_sources.resources.pqrs.anios_resource import AniosRsource

from concret_sources.resources.interrupciones.anios_resoure import AniosInterrupcion
from concret_sources.resources.interrupciones.causas_resource import CausasInterrupcion
from concret_sources.resources.interrupciones.empresas_resource import EmpresasInterrupcion
from concret_sources.resources.interrupciones.interrupciones_resource import dataInterrupcion

from concret_sources.resources.tarifarito.api_resource import apiTarifarito
from concret_sources.resources.tarifarito.users_resource import usersTarifarito
from concret_sources.resources.tarifarito.anios_resource import aniosTarifarito
from concret_sources.resources.tarifarito.empresas_resource import empresasTarifarito
from concret_sources.resources.tarifarito.mercados_resource import mercadosTarifarito
from concret_sources.resources.tarifarito.gestor.n_tolerancia_resource import gNToleranciaTarifarito
from concret_sources.resources.tarifarito.gestor.indices_dane_resource import gIDaneTarifarito
from concret_sources.resources.tarifarito.gestor.info_comercial_resource import gIComercial
from concret_sources.resources.tarifarito.gestor.resolucion_resource import gD097Resolucion
from concret_sources.resources.tarifarito.gestor.error_resource import gD097Error
from concret_sources.resources.tarifarito.gestor.perdidas_stn_resource import gPerdidasSTN
from concret_sources.resources.tarifarito.revisor.costo_unitario.costo_unitario_resource import rCostoUnitario
from concret_sources.resources.tarifarito.revisor.costo_unitario.cpteG_resource import rComponentG
from concret_sources.resources.tarifarito.revisor.costo_unitario.cpteT_resource import rComponentT
from concret_sources.resources.tarifarito.revisor.costo_unitario.cpteP097_resource import rComponentP097
from concret_sources.resources.tarifarito.revisor.costo_unitario.cpteP015_resource import rComponentP015

class SourceController():

    def __init__(self, api):
        self.__api = api
        self.__add_services()

    #--------------------------------------------------------------------------------------------
    # -- SE AGREGAN LOS SERVICIOS
    #--------------------------------------------------------------------------------------------
    def __add_services(self):
        self.__api.add_resource(apiHome, "/")
        self.__add_services_pqr()
        self.__add_services_interrupciones()
        self.__add_services_tarifarito()

    #--------------------------------------------------------------------------------------------
    # -- SERVICIOS DEL MAPA DE PQR's
    #--------------------------------------------------------------------------------------------
    def __add_services_pqr(self):
        self.__api.add_resource(PqrsRsource,
            "/pqr",

            "/pqr/<int:anio>",
            "/pqr/<int:anio>/<int:mes>",

            "/pqr/<string:servicio>",
            "/pqr/<string:servicio>/<int:anio>",
            "/pqr/<string:servicio>/<int:anio>/<int:mes>",

            "/pqr/empresa",
            "/pqr/empresa/<int:empresa>",
            "/pqr/empresa/<int:empresa>/<string:servicio>",
            "/pqr/empresa/<int:empresa>/<string:servicio>/<int:anio>",
            "/pqr/empresa/<int:empresa>/<string:servicio>/<int:anio>/<int:mes>",
            "/pqr/empresa/<int:empresa>/<string:servicio>/<int:anio>/<int:mes>/<int:causa>",

            "/pqr/centropoblado",
            "/pqr/centropoblado/<int:centropoblado>",
            "/pqr/centropoblado/<int:centropoblado>/<string:servicio>",
            "/pqr/centropoblado/<int:centropoblado>/<string:servicio>/<int:anio>",
            "/pqr/centropoblado/<int:centropoblado>/<string:servicio>/<int:anio>/<int:mes>",
        )

        self.__api.add_resource(EmpresasRsource,
            "/empresa",
            # "/empresa/<int:anio>",
            # "/empresa/<int:anio>/<int:mes>",
            "/empresa/<string:servicio>",
            # "/empresa/<string:servicio>/<int:anio>",
            # "/empresa/<string:servicio>/<int:anio>/<int:mes>",
        )

        self.__api.add_resource(CausasRsource,
            "/causas",
            "/causas/<string:servicio>",
            "/causas/<int:empresa>/<string:servicio>/<int:anio>/<int:mes>",
        )

        self.__api.add_resource(PqrsCausasRsource,
            "/pqr_causas",
            "/pqr_causas/<int:empresa>/<string:servicio>/<int:anio>/<int:mes>/<int:causa>",
        )
        
        self.__api.add_resource(AniosRsource,
            "/anios",
            "/anios/<int:anio>",
        )

    #--------------------------------------------------------------------------------------------
    # -- SERVICIOS DEL MAPA DE INTERRUPCIONES
    #--------------------------------------------------------------------------------------------
    def __add_services_interrupciones(self):
        self.__api.add_resource(AniosInterrupcion,
            "/i_anios",
            "/i_anios/<int:anio>",
        )
        
        self.__api.add_resource(CausasInterrupcion,
            "/i_causas",
            "/i_causas/<int:causa>",
        )
        
        self.__api.add_resource(EmpresasInterrupcion,
            "/i_empresas",
            "/i_empresas/<int:empresa>",
        )

        self.__api.add_resource(dataInterrupcion,
            "/i_interrupcion",
            "/i_interrupcion/<int:anio>",
            "/i_interrupcion/<int:anio>/<int:mes>",
            "/i_interrupcion/<int:anio>/<int:mes>/<int:empresa>",			
            "/i_interrupcion/<int:anio>/<int:mes>/<int:empresa>/<int:causa>",
    )
            
    #--------------------------------------------------------------------------------------------		
    # -- SERVICIOS DEL TARIFARITO
    #--------------------------------------------------------------------------------------------
    def __add_services_tarifarito(self):
        path = "/tarifarito/api"
        self.__api.add_resource(apiTarifarito,
            path + "/",
        )
        self.__api.add_resource(usersTarifarito,
            path + "/users",
            path + "/users/<int:user>",
        )
        self.__api.add_resource(aniosTarifarito,
            path + "/anios",
            path + "/anios/<int:anio>",
        )
        self.__api.add_resource(empresasTarifarito,
            path + "/empresas",
            path +  "/empresas/<int:empresa>",
        )		
        self.__api.add_resource(mercadosTarifarito,
            path + "/mercados",
            path +  "/mercados/<int:mercado>",
        )
        self.__add_services_gestor(path)
        self.__add_services_revisor(path)
    
    #--------------------------------------------------------------------------------------------		
    # -- SERVICIOS DEL GESTOR DEL TARIFARITO
    #--------------------------------------------------------------------------------------------
    def __add_services_gestor(self, path):
        self.__api.add_resource(gNToleranciaTarifarito,
            path + "/g_ntolerancia",
            path + "/g_ntolerancia/<int:anio>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
        
        self.__api.add_resource(gIDaneTarifarito,
            path + "/g_idane",
            path + "/g_idane/<int:anio>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self.__api.add_resource(gIComercial,
            path + "/g_icomercial",
            path + "/g_icomercial/<int:anio>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self.__api.add_resource(gD097Resolucion,
            path + "/g_resolucion",
            path + "/g_resolucion/<int:anio>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self.__api.add_resource(gD097Error,
            path + "/g_error",
            path + "/g_error/<string:f_inicial>",
            path + "/g_error/<string:f_inicial>/<string:f_final>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
        
        self.__api.add_resource(gPerdidasSTN,
            path + "/g_perdidasSTN",
            path + "/g_perdidasSTN/<int:anio>",
            path + "/g_perdidasSTN/<int:anio>/<string:mercado>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
    
    #--------------------------------------------------------------------------------------------		
    # -- SERVICIOS DEL REVISOR DEL TARIFARITO
    #--------------------------------------------------------------------------------------------
    def __add_services_revisor(self, path):
        self.__api.add_resource(rCostoUnitario,
            path + "/r_cunitario",
            path + "/r_cunitario/<int:anio>/<int:mes>",
            path + "/r_cunitario/<int:anio>/<int:mes>/<int:empresa>",
            path + "/r_cunitario/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>",
            path + "/r_cunitario/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>/<string:ntprop>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self.__api.add_resource(rComponentG,
            path + "/r_componentg",
            path + "/r_componentg/<int:anio>/<int:mes>/<int:empresa>",
            path + "/r_componentg/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
        
        self.__api.add_resource(rComponentT,
            path + "/r_componentT",
            path + "/r_componentT/<int:anio>/<int:mes>/<int:empresa>",
            path + "/r_componentT/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>",
            path + "/r_componentT/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>/<string:ntprop>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
        
        self.__api.add_resource(rComponentP097,
            path + "/r_componentP097",
            path + "/r_componentP097/<int:anio>/<int:mes>/<int:empresa>",
            path + "/r_componentP097/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
        
        self.__api.add_resource(rComponentP015,
            path + "/r_componentP015",
            path + "/r_componentP015/<int:anio>/<int:mes>/<int:empresa>",
            path + "/r_componentP015/<int:anio>/<int:mes>/<int:empresa>/<int:mercado>",
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
