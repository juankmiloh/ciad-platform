from concret_sources.resources.home_resources import apiHome

from concret_sources.resources.pqrs.pqrs_resource import PqrsRsource
from concret_sources.resources.pqrs.empresas_resource import EmpresasRsource
from concret_sources.resources.pqrs.causas_resource import CausasRsource
from concret_sources.resources.pqrs.pqrs_causas_resource import PqrsCausasRsource
from concret_sources.resources.pqrs.anios_resource import AniosRsource

from concret_sources.resources.interrupciones.anios_resoure import AniosInterrupcion
from concret_sources.resources.interrupciones.causas_resource import CausasInterrupcion
from concret_sources.resources.interrupciones.empresas_resource import EmpresasInterrupcion
from concret_sources.resources.interrupciones.interrupciones_resource import dataInterrupcion

from concret_sources.resources.tarifarito.api_resources import apiTarifarito
from concret_sources.resources.tarifarito.users_resources import usersTarifarito
from concret_sources.resources.tarifarito.anios_resources import aniosTarifarito
from concret_sources.resources.tarifarito.empresas_resource import empresasTarifarito
from concret_sources.resources.tarifarito.gestor.n_tolerancia_resources import gNToleranciaTarifarito
from concret_sources.resources.tarifarito.gestor.indices_dane import gIDaneTarifarito
from concret_sources.resources.tarifarito.gestor.info_comercial import gIComercial
from concret_sources.resources.tarifarito.gestor.resolucion import gD097Resolucion

class SourceController():

	def __init__(self, api):
		self.__api = api
		self.__add_services()

	# Se agregan los servicios
	def __add_services(self):
		self.__api.add_resource(apiHome, "/")
		self.__add_services_pqr()
		self.__add_services_interrupciones()
		self.__add_services_tarifarito()

	# Servicios del mapa de PQR´s
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

	# Servicios del mapa de interrupciones
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
    		
	# Servicios del TARIFARITO
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

		self.__api.add_resource(gNToleranciaTarifarito,
			path + "/n_tolerancia",
			path + "/n_tolerancia/<int:anio>",
			methods=['GET', 'POST', 'PUT', 'DELETE']
		)
		
		self.__api.add_resource(gIDaneTarifarito,
			path + "/i_dane",
			path + "/i_dane/<int:anio>",
			methods=['GET', 'POST', 'PUT', 'DELETE']
		)

		self.__api.add_resource(gIComercial,
			path + "/i_comercial",
			path + "/i_comercial/<int:anio>",
			methods=['GET', 'POST', 'PUT', 'DELETE']
		)

		self.__api.add_resource(gD097Resolucion,
			path + "/resolucion",
			path + "/resolucion/<int:anio>",
			methods=['GET', 'POST', 'PUT', 'DELETE']
		)