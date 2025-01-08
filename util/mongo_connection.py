import pymongo

def create_mongo_connection(host):
    return pymongo.MongoClient(host)