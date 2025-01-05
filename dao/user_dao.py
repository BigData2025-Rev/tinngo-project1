from model.user import User
from util import get_connection

class UserDAO:
    def __init__(self):
        self.db_conn = get_connection('sql')
        self.cursor = self.db_conn.cursor()
        self._create_user_table()

    def _create_user_table(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL,
                is_admin TINYINT(1) NOT NULL CHECK (is_admin IN (0, 1)) DEFAULT 0
            )
        '''
        self.cursor.execute(create_table_query)
        self.db_conn.commit()

    def register(self, username, password):
        check_exist_query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(check_exist_query, (username,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            return False

        insert_user_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.cursor.execute(insert_user_query, (username, password))
        self.db_conn.commit()
        return True

    def login(self, username, password):
        get_user_query = "SELECT username, is_admin FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(get_user_query, (username, password))
        user_data = self.cursor.fetchone()

        if user_data:
            print(user_data)
            user = User(*user_data)
            print(user)
            return user
        else:
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
