from dataclasses import dataclass

@dataclass
class Book:
    isbn: str = ""
    title: str = ""
    author: str = ""
    year: int = 0
    description: str = ""
