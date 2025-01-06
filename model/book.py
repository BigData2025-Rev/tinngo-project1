from dataclasses import dataclass

@dataclass
class Book:
    isbn: str = ""
    title: str = ""
    author: str = ""
    year: int = 0
    description: str = ""

    def info(self):
        return f"'{self.title}' by {self.author}"

    def detailed_info(self):
        return (
            f"ISBN: {self.isbn}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Year: {self.year}\n"
            f"Description: {self.description}\n"
        )