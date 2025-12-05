# storage.py
import json
import os
from typing import Dict, List, Optional

from models import Magazine, VALID_CATEGORIES


class MagazineStorage:
    """
    Handles loading/saving magazines from/to a JSON file.
    Internally stores magazines in a dict: id -> Magazine.
    """

    def __init__(self, file_path: str = "magazines.json") -> None:
        self.file_path = file_path
        self._items: Dict[int, Magazine] = {}
        self._next_id: int = 1
        self.load_from_file()

    # -------- Persistence --------

    def load_from_file(self) -> None:
        if not os.path.exists(self.file_path):
            self._items = {}
            self._next_id = 1
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Start fresh if file is broken
            self._items = {}
            self._next_id = 1
            return

        self._items = {}
        max_id = 0
        for item_dict in raw:
            mag = Magazine.from_dict(item_dict)
            self._items[mag.id] = mag
            max_id = max(max_id, mag.id)
        self._next_id = max_id + 1

    def save_to_file(self) -> None:
        data = [mag.to_dict() for mag in self._items.values()]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # -------- Helpers --------

    def _generate_id(self) -> int:
        new_id = self._next_id
        self._next_id += 1
        return new_id

    # -------- CRUD operations --------

    def get_all(self) -> List[Magazine]:
        return list(self._items.values())

    def get_by_category(self, category: str) -> List[Magazine]:
        return [
            m for m in self._items.values()
            if m.category.lower() == category.lower()
        ]

    def find_by_title_exact(self, title: str) -> List[Magazine]:
        return [m for m in self._items.values() if m.title == title]

    def get_by_id(self, mag_id: int) -> Optional[Magazine]:
        return self._items.get(mag_id)

    def add_magazine(
        self,
        title: str,
        publication_date: str,
        editor: str,
        category: str,
    ) -> Magazine:
        if category not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'")
        new_id = self._generate_id()
        mag = Magazine(
            id=new_id,
            title=title,
            publication_date=publication_date,
            editor=editor,
            category=category,
        )
        self._items[new_id] = mag
        self.save_to_file()
        return mag

    def delete_magazine(self, mag_id: int) -> None:
        if mag_id not in self._items:
            raise KeyError(f"Magazine with id={mag_id} does not exist")
        del self._items[mag_id]
        self.save_to_file()
