from dao import UserDAO, BookDAO
from log import logger
from util.utils import get_input, clear_screen, print_header
from model import User, Book

class LibraryCLI:
    def __init__(self):
        self.user_dao = UserDAO()
        self.book_dao = BookDAO()
        self.user: User = None

    def run(self):
        logger.info("Program started...")

        curr_state = "welcome"
        while True:
            clear_screen()
            if curr_state == "welcome":
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
                    print("Dashboard")
                    input()
                    break

            elif curr_state == "add book":
                curr_state = self.add_book()

            elif curr_state == "grant admin":
                curr_state = self.grant_admin_access()

            else:
                print(f"Unknown state: {curr_state}")
                break

        logger.info("Program ended.")

    def welcome(self):
        print_header("Welcome To Library App")
        print("[1] Log in")
        print("[2] Create new account")
        print()

        options = {"1": "login", "2": "register"}
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

        print("[1] Add book")
        print("[2] Grant admin access")
        print()

        options = {"1": "add book", "2": "grant admin"}
        choice = get_input("> ", options=options.keys())

        return options[choice]

    def add_book(self):
        print_header("Admin Dashboard: Add Book")
        while True:
            new_book = Book()
            new_book.isbn = int(input("ISBN: "))
            new_book.title = input("Title: ")
            new_book.author = input("Author: ")
            new_book.year = int(input("Year: "))
            new_book.description = input("Description: ")

            success = self.book_dao.add_book(new_book)
            if success:
                print("\nSuccessfully add book to db.")
            else:
                print("\nFailed to add book to db.")

            choice = get_input("Continue adding books? (y/n): ", options=["y", "n"])

            if choice == "n":
                break
                
            print()

        return "dashboard"

    def grant_admin_access(self):
        print_header("Admin Dashboard: Grant Admin Access")
        input()

        return ""

    def close(self):
        logger.info("Closing resources...")

        if self.user_dao:
            self.user_dao.close()
        if self.book_dao:
            self.book_dao.close()

        logger.info("Done closing resources.")

if __name__ == "__main__":
    app = LibraryCLI()
    app.run()
    app.close()
