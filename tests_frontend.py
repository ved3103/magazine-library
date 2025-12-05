# tests_frontend.py
import unittest

from client import format_magazine_for_list


class FrontendMagazineTests(unittest.TestCase):
    def test_format_magazine_for_list(self):
        item = {
            "id": 7,
            "title": "Fashion Monthly",
            "category": "Fashion",
            "editor": "Style Team",
            "publication_date": "2025-04-01",
        }
        result = format_magazine_for_list(item)
        self.assertEqual(result, "7: Fashion Monthly (Fashion)")


if __name__ == "__main__":
    unittest.main()
