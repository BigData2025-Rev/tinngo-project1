from dataclasses import dataclass

@dataclass
class Review:
    book_isbn: str = ""
    username: str = ""
    rating: int = 0
    content: str = ""

    def __repr__(self):
        return (
            "==================\n"
            f"{self.username}: {self.rating}/5\n"
            f"  {self.content}"
        )
