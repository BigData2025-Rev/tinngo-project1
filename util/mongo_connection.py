import sys
import pymongo
from log import logger

def create_mongo_connection(host):
    try:
        client = pymongo.MongoClient(host)
        logger.info("Successfully connected to MongoDB database")
        return client

    except Exception as e:
        logger.exception("""Failed to connect to MongoDB database
            host=%s
        """, host)
        logger.exception("Exception: %s", e)

        logger.info("Closing program.")
        sys.exit(1)

    return None