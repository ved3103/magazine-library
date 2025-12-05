# tests_backend.py
import unittest
import json

from backend import app, storage


class BackendMagazineTests(unittest.TestCase):
    def setUp(self):
        # clear storage
        storage._items.clear()
        storage._next_id = 1
        self.client = app.test_client()

    def test_create_and_list_magazine(self):
        payload = {
            "title": "Business Weekly",
            "publication_date": "2025-01-01",
            "editor": "Editorial Board",
            "category": "Business",
        }
        resp = self.client.post(
            "/magazines",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)

        resp = self.client.get("/magazines")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Business Weekly")

    def test_category_filter(self):
        self.client.post(
            "/magazines",
            data=json.dumps({
                "title": "Tech Today",
                "publication_date": "2025-02-01",
                "editor": "Tech Team",
                "category": "Tech",
            }),
            content_type="application/json",
        )
        self.client.post(
            "/magazines",
            data=json.dumps({
                "title": "Science World",
                "publication_date": "2025-03-01",
                "editor": "Science Team",
                "category": "Science",
            }),
            content_type="application/json",
        )

        resp = self.client.get("/magazines/category/Tech")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "Tech")


if __name__ == "__main__":
    unittest.main()
