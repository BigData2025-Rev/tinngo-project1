# Load data from books.csv into db, retrieived from
# https://www.kaggle.com/datasets/saurabhbagchi/books-dataset
import pandas as pd
from dao import BookDAO, MBookDAO
from model import Book

if __name__ == "__main__":
    file_path = "data/books.csv"
    amount = 18

    book_dao = BookDAO()
    mbook_dao = MBookDAO()

    df = pd.read_csv(file_path, nrows=amount, sep=";", dtype=str, on_bad_lines="skip", encoding_errors="ignore")

    def process(row):
        new_book = Book()
        new_book.isbn = row.iloc[0]
        new_book.title = row.iloc[1].title()
        new_book.author = row.iloc[2].title()
        new_book.year = int(row.iloc[3])
        new_book.description = f"Published by {row.iloc[4].title()}"
        print(new_book)
        book_dao.add_book(new_book)
        mbook_dao.add_book(new_book)


    df.apply(process, axis=1)

    book_dao.close()
    mbook_dao.close()
