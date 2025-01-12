import os
from dotenv import load_dotenv

load_dotenv(override=True)

from dao import UserDAO, BookDAO, BorrowDAO, ReviewDAO, MUserDAO, MBookDAO, MBorrowDAO
from log import logger
from util.utils import get_input, clear_screen, print_header, browse_books
from model import User, Book, Review


class LibraryCLI:
    def __init__(self):
        db_type = os.getenv("DB_TYPE")
        if db_type == "mysql":
            self.user_dao = UserDAO()
            self.book_dao = BookDAO()
            self.borrow_dao = BorrowDAO()
            self.review_dao = ReviewDAO()

        elif db_type == "mongodb":
            self.user_dao = MUserDAO()
            self.book_dao = MBookDAO()
            self.borrow_dao = MBorrowDAO()

        self.user: User = None

    def run(self):
        logger.info("Program started...")

        curr_state = "welcome"
        while True:
            clear_screen()
            if curr_state == "welcome":
                self.user: User = None
                curr_state = self.welcome()

            elif curr_state == "login":
                curr_state = self.login()

            elif curr_state == "register":
                curr_state = self.register()

            elif curr_state == "exit":
                print("Bye!")
                break

            elif curr_state == "dashboard":
                if self.user.is_admin:
                    curr_state = self.admin_dashboard()
                else:
                    curr_state = self.user_dashboard()

            elif curr_state == "add book":
                curr_state = self.add_book()

            elif curr_state == "grant admin":
                curr_state = self.grant_admin_access()

            elif curr_state == "borrow books":
                curr_state = self.borrow_books()

            elif curr_state == "return books":
                curr_state = self.return_books()

            elif curr_state == "review books":
                curr_state = self.review_books()

            elif curr_state == "remove review":
                curr_state = self.remove_review()

            else:
                print(f"Unknown state: {curr_state}")
                break

        logger.info("Program ended.")

    def welcome(self):
        print_header("Welcome To Library App")
        print("[1] Log in")
        print("[2] Create new account")
        print("[3] Exit")
        print()

        options = {"1": "login", "2": "register", "3": "exit"}
        choice = get_input("> ", options=options.keys())

        return options[choice]

    def login(self):
        print_header("Log In")

        while True:
            username = input("Username: ")
            password = input("Password: ")
            user = self.user_dao.login(username, password)

            if user:
                self.user = user
                break

            print("\nInvalid username/password. Please try again.\n")

        return "dashboard"

    def register(self):
        print_header("Create New Account")

        while True:
            username = input("Username: ")
            password = input("Password: ")

            if len(username) == 0 or len(password) == 0:
                print("Username/password cannot be empty. Please try again.\n")
                continue

            success = self.user_dao.register(username, password)

            if success:
                self.user = self.user_dao.login(username, password)
                return "dashboard"

            choice = get_input("Username already exists, go to login instead? (y/n): ", options=["y", "n"])

            if choice == "y":
                return "login"

            print()

    def admin_dashboard(self):
        print_header("Admin Dashboard")

        print("[1] Borrow books")
        print("[2] Return books")
        print("[3] Review books")
        print("[4] Add book")
        print("[5] Remove review")
        print("[6] Grant admin access")
        print("[7] Log out")
        print()

        options = {
            "1": "borrow books",
            "2": "return books",
            "3": "review books",
            "4": "add book",
            "5": "remove review",
            "6": "grant admin",
            "7": "welcome"
        }
        choice = get_input("> ", options=options.keys())

        return options[choice]

    def add_book(self):
        print_header("Admin Dashboard: Add Book")

        while True:
            new_book = Book()
            new_book.isbn = input("ISBN: ")
            new_book.title = input("Title: ")
            new_book.author = input("Author: ")
            new_book.year = int(input("Year: "))
            new_book.description = input("Description: ")

            success = self.book_dao.add_book(new_book)
            if success:
                print("\nSuccessfully add book to db.")
            else:
                print("\nFailed to add book to db.")

            choice = get_input("Continue? (y/n): ", options=["y", "n"])
            if choice == "n":
                break

            print()

        return "dashboard"

    def grant_admin_access(self):
        print_header("Admin Dashboard: Grant Admin Access")

        while True:
            username = input("Username: ")

            success = self.user_dao.grant_admin_access(username)
            if success:
                print(f"Successfully grant {username} admin access.")
            else:
                print(f"Invalid username {username}. Please try again.")

            choice = get_input("\nContinue? (y/n): ", options=["y", "n"])
            if choice == "n":
                break

            print()
        return "dashboard"

    def user_dashboard(self):
        print_header("Dashboard")

        print("[1] Borrow books")
        print("[2] Return books")
        print("[3] Review books")
        print("[4] Log out")
        print()

        options = {
            "1": "borrow books",
            "2": "return books",
            "3": "review books",
            "4": "welcome"
        }
        choice = get_input("> ", options=options.keys())

        return options[choice]

    def borrow_books(self):
        browse = browse_books(self.book_dao, "Borrow Books")
        first, last = next(browse)
        print("[D] Dashboard\n")

        while True:
            user_input = input("> ")
            if user_input in [">", "<"]:
                first, last = browse.send(user_input)
                print("[D] Dashboard\n")

            elif user_input == "exit":
                return "exit"
            elif user_input.lower() == "d":
                return "dashboard"
            else:
                try:
                    i = int(user_input)
                    if i < first or i > last:
                        raise ValueError

                    book = browse.send(i)
                    clear_screen()
                    print_header("Book Information")
                    print(book.detailed_info())

                    borrow_choice = get_input("Borrow? (y/n): ", options=["y", "n"])
                    if borrow_choice == "y":
                        success = self.borrow_dao.borrow_book(book.isbn, self.user.username)
                        if success:
                            print("Successly borrowed book.")
                        else:
                            print("You already borrowed this book.")
                        input("Press any key to continue...")

                    first, last = next(browse)
                    print("[D] Dashboard\n")

                except ValueError:
                    print(f"Please enter a valid number in range {first}-{last}")

    def return_books(self):
        while True:
            print_header("Return Books")

            borrowed_books_data = self.borrow_dao.get_borrowed_books(self.user.username)

            borrowed_books = [Book(*data) for data in borrowed_books_data]

            for i, book in enumerate(borrowed_books):
                print(f"[{i+1:02}] {book.info()}")

            print("\n[D] Dashboard\n")

            user_input = input("> ")
            if user_input.lower() == "d":
                return "dashboard"
            else:
                try:
                    i = int(user_input)
                    if i < 0 or i > len(borrowed_books):
                        raise ValueError

                    success = self.borrow_dao.return_book(borrowed_books[i-1].isbn, self.user.username)
                    if success:
                        print("Successly returned book.")
                    else:
                        print("Fail.")
                    input("Press any key to continue...")

                except ValueError:
                    print(f"Please enter a valid number in range {1:02}-{len(borrowed_books):02}")

            clear_screen()

        return "dashboard"

    def review_books(self):
        browse = browse_books(self.book_dao, "Review Books")
        first, last = next(browse)
        print("[D] Dashboard\n")

        while True:
            user_input = input("> ")
            if user_input in [">", "<"]:
                first, last = browse.send(user_input)
                print("[D] Dashboard\n")

            elif user_input == "exit":
                return "exit"
            elif user_input.lower() == "d":
                return "dashboard"
            else:
                try:
                    i = int(user_input)
                    if i < first or i > last:
                        raise ValueError

                    book = browse.send(i)
                    clear_screen()
                    print_header("Book Information")
                    print(book.detailed_info())

                    reviews = self.review_dao.get_reviews(book.isbn)
                    if len(reviews) == 0:
                        print("No reviews yet.")
                    else:
                        for r in reviews:
                            print(Review(*r))

                    print()

                    review_choice = get_input("Write a review? (y/n): ", options=["y", "n"])
                    if review_choice == "y":
                        print()

                        new_review = Review()
                        new_review.book_isbn = book.isbn
                        new_review.username = self.user.username
                        new_review.rating = int(get_input("Rating (1-5): ", options=["1", "2", "3", "4", "5"]))
                        new_review.content = input("Content: ")

                        success = self.review_dao.add_review(new_review)
                        if success:
                            print("Successly added review.")
                        else:
                            print("Fail to add review.")
                        input("Press any key to continue...")

                    first, last = next(browse)
                    print("[D] Dashboard\n")

                except ValueError:
                    print(f"Please enter a valid number in range {first}-{last}")

    def remove_review(self):
        browse = browse_books(self.book_dao, "Delete Review")
        first, last = next(browse)
        print("[D] Dashboard\n")

        while True:
            user_input = input("> ")
            if user_input in [">", "<"]:
                first, last = browse.send(user_input)
                print("[D] Dashboard\n")

            elif user_input == "exit":
                return "exit"
            elif user_input.lower() == "d":
                return "dashboard"
            else:
                try:
                    i = int(user_input)
                    if i < first or i > last:
                        raise ValueError

                    book = browse.send(i)
                    clear_screen()
                    print_header("Book Information")
                    print(book.detailed_info())

                    reviews = self.review_dao.get_reviews(book.isbn)
                    if len(reviews) == 0:
                        print("No reviews yet.")
                    else:
                        for r in reviews:
                            print(Review(*r))

                    print()
                    
                    username = input("Delete review of user: ")
                    success = self.review_dao.remove_review(book.isbn, username)
                    if success:
                        print("Successly remove review.")
                    else:
                        print("Fail to remove review.")
                    input("Press any key to continue...")

                    first, last = next(browse)
                    print("[D] Dashboard\n")

                except ValueError:
                    print(f"Please enter a valid number in range {first}-{last}")

    def close(self):
        logger.info("Closing resources...")

        if self.user_dao:
            self.user_dao.close()
        if self.book_dao:
            self.book_dao.close()
        if self.borrow_dao:
            self.borrow_dao.close()
        if self.review_dao:
            self.review_dao.close()

        logger.info("Done closing resources.")

if __name__ == "__main__":
    app = LibraryCLI()
    app.run()
    app.close()
