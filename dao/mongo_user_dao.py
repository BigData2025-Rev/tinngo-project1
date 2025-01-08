import os
from log import logger
from model import User
from util import get_connection

class MUserDAO:
    def __init__(self):
        logger.info("Init Mongo UserDAO...")
        self.connection = get_connection("mongodb")
        db = os.getenv("MONGODB_DATABASE")
        self.collection = self.connection[db]["User"]

    def register(self, username, password):
        logger.info("Registering new user...")

        exist = self._user_exist(username)
        if exist:
            logger.info("Failed, username exists.")
            return False

        self.collection.insert_one({
            "username": username,
            "password": password,
            "is_admin": False
        })

        logger.info("Successfully registered new user.")
        return True

    def login(self, username, password):
        logger.info("Logging in...")

        user_data = self.collection.find_one({
            "username": username,
            "password": password,
        }, {"_id": 0, "username": 1, "is_admin": 1})

        if user_data:
            user = User(*user_data.values())
            logger.info("Success, %s.", user)
            return user
        else:
            logger.info("Fail, invalid username/password.")
            return None

    def grant_admin_access(self, username):
        logger.info("Grantin admin access to %s...", username)

        exist = self._user_exist(username)
        if not exist:
            logger.info("Failed, username not exists.")
            return False

        self.collection.update_one(
            {"username": username},
            {"$set": {"is_admin": True}}
        )

        return True

    def _user_exist(self, username):
        logger.info("Getting user %s...", username)

        user = self.collection.find_one({"username": username})

        if user:
            return True

        return False

    def close(self):
        if self.connection is not None:
            self.connection.close()
