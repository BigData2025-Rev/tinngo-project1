from log import logger
from model import User
from util import get_connection

class UserDAO:
    def __init__(self):
        logger.info("Init UserDAO...")
        self.db_conn = get_connection("mysql")
        self.cursor = self.db_conn.cursor()
        self._create_user_table()

    def _create_user_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(50) NOT NULL,
                is_admin TINYINT(1) NOT NULL CHECK (is_admin IN (0, 1)) DEFAULT 0
            )
        """
        self.cursor.execute(create_table_query)
        self.db_conn.commit()

    def register(self, username, password):
        logger.info("Registering new user...")

        exist = self._user_exist(username)
        if exist:
            logger.info("Failed, username exists.")
            return False

        insert_user_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(insert_user_query, (username, password))
        self.db_conn.commit()

        logger.info("Successfully registered new user.")
        return True

    def login(self, username, password):
        logger.info("Logging in...")

        get_query = "SELECT username, is_admin FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(get_query, (username, password))
        user_data = self.cursor.fetchone()

        if user_data:
            user = User(*user_data)
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

        update_query = "UPDATE users SET is_admin = 1 WHERE username = %s"
        self.cursor.execute(update_query, (username, ))
        self.db_conn.commit()

        return True

    def _user_exist(self, username):
        logger.info("Check user %s exist...", username)

        check_exist_query = "SELECT username FROM users WHERE username = %s"
        self.cursor.execute(check_exist_query, (username,))

        if self.cursor.fetchone():
            return True

        return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
