import tempfile
import unittest
from pathlib import Path

from PIL import Image

from piano_scale_renderer import (
    WHITE,
    detect_geometry,
    hex_to_rgb,
    load_scales,
    load_tonality_colors,
    render_scale,
)

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "official_template.png"
SCALES = ROOT / "pentatonic_scales.json"
COLORS = ROOT.parents[1] / "data" / "music-theory" / "tonality-colors.json"


class PentatonicRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scales = load_scales(SCALES)
        cls.template = Image.open(TEMPLATE).convert("RGB")
        cls.geom = detect_geometry(cls.template)
        cls.colors = load_tonality_colors(COLORS)

    def render(self, name):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        out = Path(td.name) / self.scales[name]["filename"]
        report = render_scale(
            TEMPLATE,
            self.scales[name]["notes"],
            out,
            name,
            COLORS,
        )
        return Image.open(out).convert("RGB"), report

    def test_24_definitions_have_exactly_5_slots(self):
        self.assertEqual(len(self.scales), 24)
        self.assertEqual(sum("majeure" in name for name in self.scales), 12)
        self.assertEqual(sum("mineure" in name for name in self.scales), 12)
        for name, cfg in self.scales.items():
            self.assertEqual(len(cfg["notes"]), 5, name)

    def test_all_pentatonics_render_and_validate(self):
        for name in self.scales:
            with self.subTest(scale=name):
                _, report = self.render(name)
                self.assertTrue(report["ok"], report)
                self.assertEqual(report["expected_note_count"], 5)
                root = name.split()[0]
                mode = "minor" if "mineure" in name else "major"
                self.assertEqual(report["color"], self.colors[root][mode])

    def test_c_major_pentatonic_mapping(self):
        _, report = self.render("C pentatonique majeure")
        self.assertEqual(report["labels_by_slot"], {
            "C": "C", "D": "D", "E": "E", "G": "G", "A": "A"
        })

    def test_c_minor_pentatonic_mapping(self):
        _, report = self.render("C pentatonique mineure")
        self.assertEqual(report["labels_by_slot"], {
            "C": "C", "D#": "Eb", "F": "F", "G": "G", "A#": "Bb"
        })

    def test_eb_minor_uses_flat_labels_on_sharp_slots(self):
        _, report = self.render("Eb pentatonique mineure")
        self.assertEqual(report["labels_by_slot"], {
            "C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb"
        })

    def test_active_white_and_black_use_same_scale_color(self):
        image, report = self.render("D pentatonique majeure")
        expected_fill = hex_to_rgb(report["color"])

        x1, _, x2, y2 = self.geom.white_boxes["D"]
        self.assertEqual(image.getpixel(((x1 + x2) // 2, y2 - 10)), expected_fill)

        x1, _, x2, _ = self.geom.black_boxes["F#"]
        self.assertEqual(image.getpixel(((x1 + x2) // 2, 70)), expected_fill)

        x1, _, x2, y2 = self.geom.white_boxes["C"]
        self.assertEqual(image.getpixel(((x1 + x2) // 2, y2 - 10)), WHITE)

    def test_filenames_are_unique(self):
        filenames = [cfg["filename"] for cfg in self.scales.values()]
        self.assertEqual(len(filenames), len(set(filenames)))


if __name__ == "__main__":
    unittest.main()
