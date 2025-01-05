import os

def get_input(prompt, options=None):
    while True:
        user_input = input(prompt).strip().lower()

        if options is None or user_input in options:
            return user_input

        print("Invalid choice. Please try again.")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_header(text):
    width = 40

    total_pad = width - len(text)
    left_pad = total_pad // 2
    right_pad = total_pad - left_pad

    print(' ' * left_pad + text + ' ' * right_pad)
    print('-' * width)
    print()
