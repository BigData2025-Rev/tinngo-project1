from dataclasses import asdict
from log import logger
from model import Book
from util import get_connection

class BookDAO:
    def __init__(self):
        logger.info("Init BookDAO...")
        self.db_conn = get_connection("sql")
        self.cursor = self.db_conn.cursor()
        self._create_books_table()

    def _create_books_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS books (
                isbn INT PRIMARY KEY,
                title VARCHAR(50) NOT NULL,
                author VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                description VARCHAR(255) NOT NULL
            )
        """
        self.cursor.execute(create_table_query)
        self.db_conn.commit()

    def add_book(self, book: Book):
        logger.info("Adding book: %s", book)

        exist_query = "SELECT isbn FROM books WHERE isbn = %s"
        self.cursor.execute(exist_query, (book.isbn, ))
        exist = self.cursor.fetchone()
        if exist:
            logger.info("Failed to add book: duplicate ISBN.")
            return False

        add_query = "INSERT INTO books VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(add_query, tuple(asdict(book).values()))
        self.db_conn.commit()
        logger.info("Successfully added book.")

        return True

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
