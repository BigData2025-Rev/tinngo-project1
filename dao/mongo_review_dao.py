import os
from log import logger
from util import get_connection
from model import Review

class MReviewDAO:
    def __init__(self):
        logger.info("Init Mongo ReviewDAO...")
        self.connection = get_connection("mongodb")
        db = os.getenv("MONGODB_DATABASE")
        self.collection = self.connection[db]["Reviews"]

    def add_review(self, review: Review):
        logger.info("Adding review: %s", review)

        update_query = {
            "$set": {
                "rating": review.rating,
                "content": review.content
            }
        }
        filter_condition = {
            "book_isbn": review.book_isbn,
            "username": review.username
        }
        result = self.collection.update_one(filter_condition, update_query, upsert=True)

        if result.upserted_id:
            logger.info("Inserted new review with ID: %s",  result.upserted_id)
        else:
            logger.info("Successfully updated the review.")

        return True

    def get_reviews(self, book_isbn):
        k_order = ["book_isbn", "username", "rating", "content"]
        cursor = self.collection.find({"book_isbn": book_isbn}, {"_id": 0})
        results = [tuple(data[k] for k in k_order) for data in cursor]
        return results

    def remove_review(self, book_isbn, username):
        result = self.collection.delete_one({"book_isbn": book_isbn, "username": username})
        return result.deleted_count > 0

    def close(self):
        if self.connection is not None:
            self.connection.close()
