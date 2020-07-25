from ..config.oracle_connection import OracleConnection
from ..config.mongodb_connection import MongoConnection

class serviceConnection():

    def get_connectionMDB(self):
        mongodb_connection = MongoConnection()
        self.connectionMDB = mongodb_connection.get_connection()
        return self.connectionMDB

    def get_connectionSUI(self):
        oracleConnection = OracleConnection()
        self.connection = oracleConnection.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor