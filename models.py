# models.py
from dataclasses import dataclass, asdict

# Our magazine "genres"
VALID_CATEGORIES = ["Business", "Tech", "Science", "Fashion"]


@dataclass
class Magazine:
    """
    Represents a single magazine entry in the library.
    """
    id: int
    title: str
    publication_date: str
    editor: str
    category: str  # Business, Tech, Science, Fashion

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Magazine":
        return Magazine(
            id=data["id"],
            title=data["title"],
            publication_date=data["publication_date"],
            editor=data["editor"],
            category=data["category"],
        )
