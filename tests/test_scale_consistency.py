import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER_SCALES = ROOT / "tools" / "piano_scale_renderer" / "scales.json"
TRAINING_JS = ROOT / "js" / "scales_script.js"
LIBRARY_JS = ROOT / "js" / "scale_library.js"
THEORY_SCALES = ROOT / "data" / "music-theory" / "scales.json"
SCALE_IMAGES = ROOT / "images" / "Scales"

JS_SCALE_ENTRY = re.compile(
    r"\{\s*label:\s*'([^']+)'\s*,\s*image:\s*'([^']+)'\s*\}"
)

FRENCH_NOTE_NAMES = {
    "C": "Do",
    "C#": "Do♯",
    "Db": "Ré♭",
    "D": "Ré",
    "D#": "Ré♯",
    "Eb": "Mi♭",
    "E": "Mi",
    "F": "Fa",
    "F#": "Fa♯",
    "Gb": "Sol♭",
    "G": "Sol",
    "G#": "Sol♯",
    "Ab": "La♭",
    "A": "La",
    "A#": "La♯",
    "Bb": "Si♭",
    "B": "Si",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_js_scale_entries(path):
    text = path.read_text(encoding="utf-8")
    return JS_SCALE_ENTRY.findall(text)


def canonical_training_name(label):
    suffix = " mineure naturelle"
    if label.endswith(suffix):
        return label[:-len(suffix)] + " mineur naturel"
    return label


def split_renderer_name(name):
    if name.endswith(" majeur"):
        return name[:-len(" majeur")], "major"
    if name.endswith(" mineur naturel"):
        return name[:-len(" mineur naturel")], "natural_minor"
    raise AssertionError(f"Famille de gamme inattendue dans le renderer: {name}")


def expected_library_label(renderer_name):
    tonic, family = split_renderer_name(renderer_name)
    note = FRENCH_NOTE_NAMES[tonic]
    if family == "major":
        return f"{note} majeur"
    return f"{note} mineur naturel"


class ScaleSourceConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.renderer = load_json(RENDERER_SCALES)
        cls.training_entries = load_js_scale_entries(TRAINING_JS)
        cls.library_entries = load_js_scale_entries(LIBRARY_JS)
        cls.theory = load_json(THEORY_SCALES)

    def test_renderer_contract_is_12_major_plus_12_natural_minor(self):
        self.assertEqual(len(self.renderer), 24)

        majors = []
        minors = []
        for name, cfg in self.renderer.items():
            tonic, family = split_renderer_name(name)
            self.assertEqual(len(cfg["notes"]), 7, name)
            self.assertEqual(len(set(cfg["notes"].keys())), 7, name)
            self.assertEqual(len(set(cfg["notes"].values())), 7, name)
            self.assertTrue(cfg["filename"].endswith(".png"), name)

            if family == "major":
                majors.append(tonic)
            else:
                minors.append(tonic)

        self.assertEqual(len(majors), 12)
        self.assertEqual(len(minors), 12)
        self.assertEqual(len(set(majors)), 12)
        self.assertEqual(len(set(minors)), 12)

    def test_training_mapping_matches_renderer_names_and_filenames(self):
        self.assertEqual(len(self.training_entries), 24)

        labels = [label for label, _ in self.training_entries]
        images = [image for _, image in self.training_entries]
        self.assertEqual(len(set(labels)), 24, "Libellé dupliqué dans js/scales_script.js")
        self.assertEqual(len(set(images)), 24, "PNG dupliqué dans js/scales_script.js")

        actual = {
            canonical_training_name(label): image
            for label, image in self.training_entries
        }
        expected = {
            name: f"images/Scales/{cfg['filename']}"
            for name, cfg in self.renderer.items()
        }
        self.assertEqual(actual, expected)

    def test_scale_library_matches_renderer_images_and_labels(self):
        self.assertEqual(len(self.library_entries), 24)

        labels = [label for label, _ in self.library_entries]
        images = [image for _, image in self.library_entries]
        self.assertEqual(len(set(labels)), 24, "Libellé dupliqué dans js/scale_library.js")
        self.assertEqual(len(set(images)), 24, "PNG dupliqué dans js/scale_library.js")

        actual = {image: label for label, image in self.library_entries}
        expected = {
            f"images/Scales/{cfg['filename']}": expected_library_label(name)
            for name, cfg in self.renderer.items()
        }
        self.assertEqual(actual, expected)

    def test_theory_ionian_and_aeolian_match_renderer_spellings(self):
        groups = {
            "major": self.theory["ionien"],
            "natural_minor": self.theory["éolien"],
        }

        for family, items in groups.items():
            self.assertEqual(len(items), 12, family)
            tonics = [item["tonic"] for item in items]
            self.assertEqual(len(set(tonics)), 12, f"Tonique dupliquée dans {family}")
            by_tonic = {item["tonic"]: item["notes"] for item in items}

            renderer_names = {
                name: split_renderer_name(name)
                for name in self.renderer
                if split_renderer_name(name)[1] == family
            }
            expected_tonics = {tonic for tonic, _ in renderer_names.values()}
            self.assertEqual(set(by_tonic), expected_tonics)

            for renderer_name, (tonic, _) in renderer_names.items():
                notes = by_tonic[tonic]
                self.assertEqual(len(notes), 7, renderer_name)
                self.assertEqual(len(set(notes)), 7, renderer_name)
                self.assertEqual(notes[0], tonic, renderer_name)

                renderer_labels = set(self.renderer[renderer_name]["notes"].values())
                self.assertEqual(
                    set(notes),
                    renderer_labels,
                    f"Orthographe ou contenu divergent pour {renderer_name}",
                )

    def test_every_renderer_png_exists_in_live_assets(self):
        missing = [
            cfg["filename"]
            for cfg in self.renderer.values()
            if not (SCALE_IMAGES / cfg["filename"]).is_file()
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
