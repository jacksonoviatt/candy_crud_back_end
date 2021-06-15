import dbcreds
import mariadb
import traceback

# connect to the databse
def get_db_connection():
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, database=dbcreds.database, port=dbcreds.port)
        return conn
    except:
        print("ERROR connecting to the DB")
        traceback.print_exc()
        return None

# now we will connect to the cursor
def get_db_cursor(conn):
    try:
        return conn.cursor()
    except:
        print("ERROR creating cursor on DB")
        traceback.print_exc()
        return None

# disconnect to the cursor
def close_db_cursor(cursor):
    try:
        cursor.close()
        return True
    except:
        print("ERROR closing cursor on DB")
        traceback.print_exc()
        return False

# disconnect to the databse
def close_db_connection(conn):
    try:
        conn.close()
        return True
    except:
        print("ERROR closing connection to DB")
        traceback.print_exc()
        return False


