import sys
import mysql.connector
from log import logger

def create_sql_connection(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        logger.info("Successfully connected to MySQL database")
        return db_connection

    except mysql.connector.errors.ProgrammingError as e:
        logger.exception("""Failed to connect to MySQL database
            host=%s,
            user=%s,
            password=%s,
            database=%s
        """, host, user, password, database)
        logger.exception("Exception: %s", e)

        logger.info("Closing program.")
        sys.exit(1)

    return None
