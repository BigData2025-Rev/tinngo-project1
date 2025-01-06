import os
from model import Book

def get_input(prompt, options=None):
    while True:
        user_input = input(prompt).strip().lower()

        if options is None or user_input in options:
            return user_input

        print("Invalid choice. Please try again.")

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def print_header(text):
    width = 40

    total_pad = width - len(text)
    left_pad = total_pad // 2
    right_pad = total_pad - left_pad

    print(" " * left_pad + text + " " * right_pad)
    print("=" * width)
    print()

def browse_books(book_dao, header):
    page_size = 5
    generator = book_dao.get_books_in_batches(page_size)
    total = next(generator)
    curr_page = 0

    while True:
        print_header(header)

        books_data = generator.send(curr_page)
        books = [Book(*data) for data in books_data]
        for i, book in enumerate(books):
            book_i = page_size * curr_page + i + 1
            print(f"[{book_i:02}] {book.info()}")

        for i in range(page_size - len(books) + 1):
            print()

        first = (curr_page * page_size) + 1
        last = (curr_page * page_size) + len(books)
        print(f"Showing {first}-{last} out of {total} books\n")

        if last != total:
            print("[>] Next page")
        if first != 1:
            print("[<] Previous page")

        user_input = (yield (first, last))
        if user_input == ">":
            if  last != total:
                curr_page += 1
        elif user_input == "<":
            if first != 1:
                curr_page -= 1
        else:
            i = user_input % page_size - 1
            yield books[i]

        clear_screen()
