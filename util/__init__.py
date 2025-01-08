import os
import sys
from log import logger
from .sql_connection import create_sql_connection
from .mongo_connection import create_mongo_connection

def get_connection(connection_type="mysql"):
    logger.info("Requested db: %s", connection_type)

    if connection_type == "mysql":
        host = os.getenv("SQL_HOST")
        user = os.getenv("SQL_USER")
        password = os.getenv("SQL_PASSWORD")
        database = os.getenv("SQL_DATABASE")
        return create_sql_connection(host, user, password, database)

    elif connection_type == "mongodb":
        mongo_host = os.getenv("MONGODB_HOST")
        return create_mongo_connection(mongo_host)

    else:
        logger.exception("Unsupported connection type: %s", connection_type)
        logger.info("Closing program.")
        sys.exit(1)
