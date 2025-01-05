from dataclasses import dataclass

@dataclass
class Book:
    isbn: int = 0
    title: str = ""
    author: str = ""
    year: int = 0
    description: str = ""
