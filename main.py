import os
from dotenv import load_dotenv

load_dotenv(override=True)

from dao import UserDAO, BookDAO, BorrowDAO, MUserDAO, MBookDAO, MBorrowDAO
from log import logger
from util.utils import get_input, clear_screen, print_header, browse_books
from model import User, Book


class LibraryCLI:
    def __init__(self):
        db_type = os.getenv("DB_TYPE")
        if db_type == "mysql":
            self.user_dao = UserDAO()
            self.book_dao = BookDAO()
            self.borrow_dao = BorrowDAO()
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
        print("[3] Add book")
        print("[4] Grant admin access")
        print("[5] Log out")
        print()

        options = {"1": "borrow books", "2": "return books", "3": "add book", "4": "grant admin",  "5": "welcome"}
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
        print("[3] Log out")
        print()

        options = {"1": "borrow books", "2": "return books", "3": "welcome"}
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
                        input()

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
                    input()

                except ValueError:
                    print(f"Please enter a valid number in range {1:02}-{len(borrowed_books):02}")

            clear_screen()

        return "dashboard"

    def close(self):
        logger.info("Closing resources...")

        if self.user_dao:
            self.user_dao.close()
        if self.book_dao:
            self.book_dao.close()
        if self.borrow_dao:
            self.borrow_dao.close()

        logger.info("Done closing resources.")

if __name__ == "__main__":
    app = LibraryCLI()
    app.run()
    app.close()
