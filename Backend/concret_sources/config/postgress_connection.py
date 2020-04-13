import json
import psycopg2
from sqlalchemy import create_engine

# -- CLASE QUE GESTIONA LA CONEXION CON LA BASE DE DATOS POSTGRESQL
class PostgresConnection():
    def __init__(self):
        credentials = json.load(open("config/configuration.json"))
        self.connection = psycopg2.connect(
            "host='"+ credentials["postgres_credentials"]["host"] + "' " +
            "dbname='"+ credentials["postgres_credentials"]["db"] + "' " + 
            "user='"+ credentials["postgres_credentials"]["usuario"] + "' " + 
            "password='"+ credentials["postgres_credentials"]["contrasena"] + "' " + 
            "port='"+ credentials["postgres_credentials"]["port"] + "' "
        )
        print(" -- POSTGRESQL CONNECTION SUCCESFULL !!")

        self.sa_connection = create_engine( "postgresql://" +
            credentials["postgres_credentials"]["usuario"] + ":" +
            credentials["postgres_credentials"]["contrasena"] + "@" +
            credentials["postgres_credentials"]["host"] + ":" +
            credentials["postgres_credentials"]["port"] + "/" +
            credentials["postgres_credentials"]["db"]
        )
        print(" -- POSTGRESQL SQLALCHEMY CONNECTION SUCCESFULL !!")

    def get_connection(self):
        return self.connection

    def get_sqlalchemy_connection(self):
        return self.sa_connection

