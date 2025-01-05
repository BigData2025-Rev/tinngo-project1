import os
from dotenv import load_dotenv
from log import logger
from .sql_connection import create_sql_connection
from .mongo_connection import create_mongo_connection

load_dotenv()

def get_connection(connection_type="sql"):
    logger.info("Requested db: %s", connection_type)

    if connection_type == "sql":
        host=os.getenv("SQL_HOST")
        user=os.getenv("SQL_USER")
        password=os.getenv("SQL_PASSWORD")
        database=os.getenv("SQL_DATABASE")
        return create_sql_connection(host, user, password, database)
    elif connection_type == "mongodb":
        return create_mongo_connection()
    else:
        print(f"Unsupported connection type: {connection_type}")
        return None
