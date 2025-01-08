import os
from datetime import datetime, timedelta
from log import logger
from util import get_connection

class MBorrowDAO:
    def __init__(self):
        logger.info("Init Mongo BorrowDAO...")
        self.connection = get_connection("mongodb")
        db = os.getenv("MONGODB_DATABASE")
        self.collection = self.connection[db]["Borrow"]

    def borrow_book(self, book_isbn, username):
        logger.info("User %s borrowing %s...", username, book_isbn)

        exist = self.collection.find_one({"book_isbn": book_isbn, "username": username})
        if exist:
            logger.info("Failed, already borrowed.")
            return False

        borrow_date = datetime.today().date()
        borrow_date = datetime.combine(borrow_date, datetime.min.time())
        due_date = datetime.today().date() + timedelta(weeks=1)
        due_date = datetime.combine(due_date, datetime.min.time())

        self.collection.insert_one({
            "book_isbn": book_isbn,
            "username": username,
            "borrow_date": borrow_date,
            "due_date": due_date,
            "return_date": None
        })

        logger.info("Successfully borrowed.")

        return True

    def get_borrowed_books(self, username):
        logger.info("Get list of borrowed books by user %s", username)
        pipeline = [
            {
                "$lookup": {
                    "from": "Book",
                    "localField": "book_isbn",
                    "foreignField": "isbn", 
                    "as": "book_info"
                }
            },
            {
                "$unwind": "$book_info"
            },
            {
                "$match": {
                    "username": username,
                    "return_date": None
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "info": [
                        "$book_info.isbn",
                        "$book_info.title",
                        "$book_info.author",
                        "$book_info.year",
                        "$book_info.description",
                    ]
                }
            }
        ]
        books_data = self.collection.aggregate(pipeline)
        books_data = [list(data.values())[0] for data in books_data]
        return books_data

    def return_book(self, book_isbn, username):
        logger.info("User %s returning %s...", username, book_isbn)
        return_date = datetime.today().date()
        return_date = datetime.combine(return_date, datetime.min.time())

        self.collection.update_one(
            {"book_isbn": book_isbn, "username": username},
            {"$set": {"return_date": return_date}}
        )
        logger.info("Successfully returned.")

        return True

    def close(self):
        if self.connection is not None:
            self.connection.close()
