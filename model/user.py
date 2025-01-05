from dataclasses import dataclass

@dataclass
class User:
    username: str = ""
    is_admin: bool = False

    def __init__(self, username: str, is_admin: int):
        self.username = username
        self.is_admin = bool(is_admin)
