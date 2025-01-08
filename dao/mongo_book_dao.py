import os
from log import logger
from model import Book
from util import get_connection

class MBookDAO:
    def __init__(self):
        logger.info("Init Mongo BookDAO...")
        self.connection = get_connection("mongodb")
        db = os.getenv("MONGODB_DATABASE")
        self.collection = self.connection[db]["Book"]

    def add_book(self, book: Book):
        logger.info("Adding book: %s", book)

        exist = self.collection.find_one({"isbn": book.isbn})
        if exist:
            logger.info("Failed to add book: duplicate ISBN.")
            return False

        self.collection.insert_one({
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "description": book.description
        })

        logger.info("Successfully added book.")

        return True

    def get_books_in_batches(self, batch_size):
        total = self.collection.count_documents({})
        curr_page = (yield total)

        while True:
            offset = curr_page * batch_size
            books_data = self.collection.find({}, {"_id": 0}).skip(offset).limit(batch_size)
            books_data = [data.values() for data in books_data]
            curr_page = (yield books_data)

    def close(self):
        if self.connection is not None:
            self.connection.close()
