# client.py
from typing import List, Dict, Any

import requests


class MagazineClient:
    """
    Simple client used by the Tkinter GUI to call the Flask backend.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:5000") -> None:
        self.base_url = base_url.rstrip("/")

    # --- backend calls ---

    def get_all_magazines(self) -> List[Dict[str, Any]]:
        resp = requests.get(f"{self.base_url}/magazines", timeout=5)
        resp.raise_for_status()
        return resp.json()

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        resp = requests.get(
            f"{self.base_url}/magazines/category/{category}",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()

    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        params = {"title": title}
        resp = requests.get(
            f"{self.base_url}/magazines/search",
            params=params,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()

    def get_by_id(self, mag_id: int) -> Dict[str, Any]:
        resp = requests.get(f"{self.base_url}/magazines/{mag_id}", timeout=5)
        resp.raise_for_status()
        return resp.json()

    def create_magazine(self, data: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}/magazines",
            json=data,
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()

    def delete_magazine(self, mag_id: int) -> None:
        resp = requests.delete(f"{self.base_url}/magazines/{mag_id}", timeout=5)
        resp.raise_for_status()


def format_magazine_for_list(item: Dict[str, Any]) -> str:
    """
    Format one magazine for displaying in the Listbox.
    """
    return f"{item['id']}: {item['title']} ({item['category']})"
