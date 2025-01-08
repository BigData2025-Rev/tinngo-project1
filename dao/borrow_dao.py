from datetime import datetime, timedelta
from log import logger
from util import get_connection

class BorrowDAO:
    def __init__(self):
        logger.info("Init BorrowDAO...")
        self.db_conn = get_connection("mysql")
        self.cursor = self.db_conn.cursor()
        self._create_borrow_table()

    def _create_borrow_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS borrow (
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_isbn VARCHAR(13) NOT NULL,
                username VARCHAR(50) NOT NULL,
                borrow_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                FOREIGN KEY (book_isbn) REFERENCES books(isbn),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """
        self.cursor.execute(create_table_query)
        self.db_conn.commit()

    def borrow_book(self, book_isbn, username):
        exist_query = "SELECT * FROM borrow WHERE book_isbn = %s AND username = %s AND return_date IS NULL"
        self.cursor.execute(exist_query, (book_isbn, username))
        exist = self.cursor.fetchone()
        if exist:
            return False

        borrow_date = datetime.today().date()
        due_date = datetime.today().date() + timedelta(weeks=1)
        self.cursor.execute("INSERT INTO borrow (book_isbn, username, borrow_date, due_date) VALUES (%s, %s, %s, %s)", (book_isbn, username, borrow_date, due_date))
        self.db_conn.commit()

        return True

    def get_borrowed_books(self, username):
        exist_query = "SELECT books.* FROM books, borrow WHERE books.isbn = borrow.book_isbn AND borrow.username = %s AND borrow.return_date IS NULL"
        self.cursor.execute(exist_query, (username,))
        return self.cursor.fetchall()

    def return_book(self, book_isbn, username):
        return_date = datetime.today().date()
        update_query = "UPDATE borrow SET return_date = %s WHERE book_isbn = %s AND username = %s AND return_date IS NULL"
        self.cursor.execute(update_query, (return_date, book_isbn, username))
        self.db_conn.commit()

        return True

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
