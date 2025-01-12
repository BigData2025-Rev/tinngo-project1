from dataclasses import asdict
from log import logger
from model import Review
from util import get_connection

class ReviewDAO:
    def __init__(self):
        logger.info("Init ReviewDAO...")
        self.db_conn = get_connection("mysql")
        self.cursor = self.db_conn.cursor()
        self._create_reviews_table()

    def _create_reviews_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_isbn VARCHAR(13) NOT NULL,
                username VARCHAR(50) NOT NULL,
                rating INT NOT NULL,
                content VARCHAR(255) NOT NULL,
                FOREIGN KEY (book_isbn) REFERENCES books(isbn),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """
        self.cursor.execute(create_table_query)
        self.db_conn.commit()

    def add_review(self, review: Review):
        logger.info("Adding review: %s", review)

        self.cursor.execute("""
            UPDATE reviews 
            SET rating = %s, content = %s 
            WHERE book_isbn = %s AND username = %s
        """, (review.rating, review.content, review.book_isbn, review.username))
        self.db_conn.commit()

        if self.cursor.rowcount == 0:
            self.cursor.execute("""
                INSERT INTO reviews
                VALUES (NULL, %s, %s, %s, %s)
            """, tuple(asdict(review).values()))
            self.db_conn.commit()

        logger.info("Successfully added review.")

        return True

    def get_reviews(self, book_isbn):
        self.cursor.execute("""
            SELECT book_isbn, username, rating, content
            FROM reviews
            WHERE book_isbn = %s
        """, (book_isbn ,))
        return self.cursor.fetchall()

    def remove_review(self, book_isbn, username):
        self.cursor.execute("""
            DELETE FROM reviews
            WHERE book_isbn = %s and username = %s
        """, (book_isbn, username))
        return self.cursor.rowcount > 0

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
