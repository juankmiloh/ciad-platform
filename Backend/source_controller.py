from concret_sources.pqrs_resource import PqrsRsource
from concret_sources.empresas_resource import EmpresasRsource
from concret_sources.causas_resource import CausasRsource
from concret_sources.pqrs_causas_resource import PqrsCausasRsource
from concret_sources.anios_resource import AniosRsource


class SourceController():

	def __init__(self, api):
		self.__api = api
		self.__add_services()

	def __add_services(self):
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