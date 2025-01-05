from dao.user_dao import UserDAO
from util.utils import get_input, clear_screen, print_header

class LibraryCLI:
    def __init__(self):
        self.user_dao = UserDAO()
        self.user = None

    def run(self):
        curr_state = 'welcome'
        while True:
            clear_screen()
            if curr_state == 'welcome':
                curr_state = self.welcome()

            elif curr_state == 'login':
                curr_state = self.login()

            elif curr_state == 'register':
                curr_state = self.register()

            elif curr_state == 'exit':
                print("Bye!")
                break

            elif curr_state == 'dashboard':
                if self.user.is_admin:
                    print("Admin Dashboard")
                else:
                    print("Dashboard")

                input()
                break

            else:
                raise Exception(f"Unknown state: {curr_state}")

    def welcome(self):
        print_header("Welcome to the Library CLI App")
        print("[1] Log in")
        print("[2] Create new account")
        print()

        options = {'1': "login", "2": "register"}
        choice = get_input("> ", options=options.keys())
        print(options[choice])

        return options[choice]

    def login(self):
        print_header("Log in")

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
        print_header("Create new account")

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

    def close(self):
        if self.user_dao:
            self.user_dao.close()

if __name__ == "__main__":
    app = LibraryCLI()
    app.run()
    app.close()
