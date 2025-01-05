import mysql.connector

def create_sql_connection(host, user, password, database):
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if db_connection.is_connected():
        print("Successfully connected to MySQL database")
    else:
        raise Exception("Failed to connect to MySQL database")

    return db_connection
