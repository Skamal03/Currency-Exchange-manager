import pymysql

def get_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='b0st0n',
            database='currency_exchange_manager',
        )
        print("Connection successful")
        return connection

    except pymysql.MySQLError as e:
        print("Connection failed:", e)
        return None

conn = get_connection()
if conn:
    conn.close()
