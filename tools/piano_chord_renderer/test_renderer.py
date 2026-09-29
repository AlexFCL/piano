import tempfile
import unittest
from pathlib import Path

from PIL import Image

from piano_chord_renderer import (
    ROOT_ORDER,
    detect_geometry,
    hex_to_rgb,
    load_tonality_colors,
    render_chord,
    triad_labels,
)

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "official_template.png"
COLORS = ROOT.parents[1] / "data" / "music-theory" / "tonality-colors.json"


class ChordRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.colors = load_tonality_colors(COLORS)
        cls.template = Image.open(TEMPLATE).convert("RGB")
        cls.geom = detect_geometry(cls.template)

    def render(self, root, quality, inversion):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        out = Path(td.name) / "chord.png"
        report = render_chord(TEMPLATE, COLORS, root, quality, inversion, out)
        return Image.open(out).convert("RGB"), report

    def test_palette_has_all_17_runtime_root_spellings(self):
        for root in ROOT_ORDER:
            self.assertIn(root, self.colors)

    def test_all_102_chords_render_with_runtime_palette(self):
        for root in ROOT_ORDER:
            for quality in ("major", "minor"):
                for inversion in (0, 1, 2):
                    with self.subTest(root=root, quality=quality, inversion=inversion):
                        _, report = self.render(root, quality, inversion)
                        self.assertTrue(report["ok"])
                        self.assertEqual(len(report["active_slots"]), 3)
                        self.assertEqual(report["color"], self.colors[root][quality])

    def test_c_major_uses_runtime_major_color(self):
        image, report = self.render("C", "major", 0)
        expected_hex = self.colors["C"]["major"]
        self.assertEqual(report["color"], expected_hex)
        self.assertEqual(report["labels_by_slot"], {"C2": "C", "E2": "E", "G2": "G"})
        self.assertEqual(image.getpixel((365, 180)), hex_to_rgb(expected_hex))

    def test_c_major_inversions_match_existing_chord_logic(self):
        _, first = self.render("C", "major", 1)
        _, second = self.render("C", "major", 2)
        self.assertEqual(first["labels_by_slot"], {"E1": "E", "G1": "G", "C2": "C"})
        self.assertEqual(second["labels_by_slot"], {"G1": "G", "C2": "C", "E2": "E"})

    def test_theoretical_spelling(self):
        self.assertEqual(triad_labels("Eb", "major"), ["Eb", "G", "Bb"])
        self.assertEqual(triad_labels("D#", "major"), ["D#", "F##", "A#"])
        self.assertEqual(triad_labels("Gb", "major"), ["Gb", "Bb", "Db"])


if __name__ == "__main__":
    unittest.main()
