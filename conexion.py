import pymysql
def crear_conexion():
    try:
        connection = pymysql.connect(
            host='autorack.proxy.rlwy.net',
            user='root',
            password='lDWLBIxYCbLnYZXYqQFYLkNrTJVgQnDM',
            database='railway',
            port=36047
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar: {e}")
        return None