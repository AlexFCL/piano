import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageChops

from piano_scale_renderer import (
    BLACK,
    ORANGE,
    RED,
    WHITE,
    detect_geometry,
    load_scales,
    render_scale,
)

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "official_template.png"
SCALES = ROOT / "scales.json"


class RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scales = load_scales(SCALES)
        cls.template = Image.open(TEMPLATE).convert("RGB")
        cls.geom = detect_geometry(cls.template)

    def render(self, name):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        out = Path(td.name) / self.scales[name]["filename"]
        report = render_scale(TEMPLATE, self.scales[name]["notes"], out)
        return Image.open(out).convert("RGB"), report

    def test_all_24_scale_definitions_have_7_slots(self):
        self.assertEqual(len(self.scales), 24)
        for name, cfg in self.scales.items():
            self.assertEqual(len(cfg["notes"]), 7, name)


    def test_all_scales_render_and_validate(self):
        for name in self.scales:
            with self.subTest(scale=name):
                _, report = self.render(name)
                self.assertTrue(report["ok"], report)

    def test_golden_c_and_e_are_pixel_identical(self):
        for name in ("C majeur", "E majeur"):
            with self.subTest(scale=name):
                image, _ = self.render(name)
                golden = Image.open(ROOT / "golden" / self.scales[name]["filename"]).convert("RGB")
                self.assertIsNone(ImageChops.difference(image, golden).getbbox())

    def test_d_major_upper_d_and_e_are_fully_red(self):
        image, _ = self.render("D majeur")
        # Upper exposed regions of D and E, where the historical bug left white gaps.
        for slot in ("D", "E"):
            x1, y1, x2, _ = self.geom.white_boxes[slot]
            for y in range(y1, 120):
                for x in range(x1, x2 + 1):
                    # Skip pixels covered by black keys.
                    if any(bx1 <= x <= bx2 and by1 <= y <= by2 for bx1, by1, bx2, by2 in self.geom.black_boxes.values()):
                        continue
                    self.assertEqual(image.getpixel((x, y)), RED, (slot, x, y))

    def test_eb_major_upper_d_is_fully_red(self):
        image, _ = self.render("Eb majeur")
        x1, y1, x2, _ = self.geom.white_boxes["D"]
        for y in range(y1, 120):
            for x in range(x1, x2 + 1):
                if any(bx1 <= x <= bx2 and by1 <= y <= by2 for bx1, by1, bx2, by2 in self.geom.black_boxes.values()):
                    continue
                self.assertEqual(image.getpixel((x, y)), RED, (x, y))

    def test_db_major_mapping_is_fixed_and_not_shiftable(self):
        _, report = self.render("Db majeur")
        self.assertEqual(report["labels_by_slot"], {
            "C": "C", "C#": "Db", "D#": "Eb", "F": "F", "F#": "Gb", "G#": "Ab", "A#": "Bb"
        })

    def test_db_major_inactive_white_keys_remain_white(self):
        image, _ = self.render("Db majeur")
        for slot in ("D", "E", "G", "A", "B"):
            x1, _, x2, y2 = self.geom.white_boxes[slot]
            # Sample near bottom, away from labels and black keys.
            y = y2 - 10
            x = (x1 + x2) // 2
            self.assertEqual(image.getpixel((x, y)), WHITE, slot)

    def test_db_major_black_slots_are_orange(self):
        image, _ = self.render("Db majeur")
        for slot in ("C#", "D#", "F#", "G#", "A#"):
            x1, y1, x2, y2 = self.geom.black_boxes[slot]
            x = (x1 + x2) // 2
            y = 70
            self.assertEqual(image.getpixel((x, y)), ORANGE, slot)
            self.assertEqual(image.getpixel((x1 + 1, y)), BLACK, slot)


if __name__ == "__main__":
    unittest.main()
