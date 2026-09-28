import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES_PATH = ROOT / "data" / "categories.json"

EXPECTED_ORDER = ["accords", "gammes", "theorie", "rythme", "basse"]


class CategoryMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.categories = json.loads(CATEGORIES_PATH.read_text(encoding="utf-8"))

    def test_home_categories_are_complete_and_ordered(self):
        self.assertEqual([item["id"] for item in self.categories], EXPECTED_ORDER)

        for item in self.categories:
            for key in ("id", "title", "description", "icon", "href"):
                self.assertTrue(item.get(key), f"{item.get('id', '?')}: champ {key} manquant")

        ids = [item["id"] for item in self.categories]
        hrefs = [item["href"] for item in self.categories]
        self.assertEqual(len(ids), len(set(ids)), "Identifiant de catégorie dupliqué")
        self.assertEqual(len(hrefs), len(set(hrefs)), "Route de catégorie dupliquée")

    def test_every_home_route_points_to_an_existing_page(self):
        missing = []
        for item in self.categories:
            target = urlparse(item["href"]).path
            if not (ROOT / target).is_file():
                missing.append(target)
        self.assertEqual(missing, [])

    def test_generic_categories_match_their_query_and_exercise_file(self):
        generic = [item for item in self.categories if item.get("exerciseFile")]
        self.assertEqual({item["id"] for item in generic}, {"rythme", "basse"})

        for item in generic:
            parsed = urlparse(item["href"])
            query = parse_qs(parsed.query)
            self.assertEqual(parsed.path, "category.html")
            self.assertEqual(query.get("category"), [item["id"]])
            self.assertTrue((ROOT / item["exerciseFile"]).is_file(), item["exerciseFile"])


if __name__ == "__main__":
    unittest.main()
