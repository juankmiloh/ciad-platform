from concret_sources.pqrs.pqrs_resource import PqrsRsource
from concret_sources.pqrs.empresas_resource import EmpresasRsource
from concret_sources.pqrs.causas_resource import CausasRsource
from concret_sources.pqrs.pqrs_causas_resource import PqrsCausasRsource
from concret_sources.pqrs.anios_resource import AniosRsource

from concret_sources.interrupciones.anios_resoure import AniosInterrupcion
from concret_sources.interrupciones.causas_resource import CausasInterrupcion
from concret_sources.interrupciones.empresas_resource import EmpresasInterrupcion
from concret_sources.interrupciones.interrupciones_resource import dataInterrupcion


class SourceController():

	def __init__(self, api):
		self.__api = api
		self.__add_services()

	def __add_services(self):
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