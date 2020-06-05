import os
import json
import cx_Oracle

PATH = os.path.dirname(os.path.realpath(__file__))

class OracleConnection(): 
    def __init__(self):
        credentials = json.load(open(PATH + "/configuration_sui.json"))
        self.connection = cx_Oracle.connect(credentials["oracle_credentials"]["usuario"] + "/" +
            credentials["oracle_credentials"]["contrasena"] + "@" +
            credentials["oracle_credentials"]["host"] + ":" +
            credentials["oracle_credentials"]["port"] + "/" +
            credentials["oracle_credentials"]["SID"])
        print(" -- ORACLE CONNECTION SUCCESFULL !!")

    def get_connection(self):
        return self.connection

# oracleConnection = OracleConnection()
# connection = oracleConnection.get_connection()
# cursor = connection.cursor()
# cursor.execute('select * from dual')
# for result in cursor:
#     print(result)