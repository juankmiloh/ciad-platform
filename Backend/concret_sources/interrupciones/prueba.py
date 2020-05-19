from ..config.oracle_connection import OracleConnection

oracleConnection = OracleConnection()
connection = oracleConnection.get_connection()
cursor = connection.cursor()
cursor.execute('select * from dual')
print(cursor)