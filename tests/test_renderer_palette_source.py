from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "data" / "music-theory" / "tonality-colors.json"
SHARED_POLICY = ROOT / "docs" / "chatgpt" / "RENDERERS_SOURCE_OF_TRUTH_V1.md"
POINTER = ROOT / "CHATGPT_PROJECT_POINTER.md"

RENDERERS = [
    ROOT / "tools" / "piano_chord_renderer",
    ROOT / "tools" / "piano_scale_renderer",
]


class RendererPaletteSourceTests(unittest.TestCase):
    def test_runtime_palette_is_structurally_complete(self):
        data = json.loads(PALETTE.read_text(encoding="utf-8"))
        self.assertEqual(len(data), 12)
        for family, cfg in data.items():
            self.assertTrue(cfg["aliases"], family)
            for key in ("base", "major", "minor"):
                self.assertRegex(cfg[key], r"^#[0-9A-Fa-f]{6}$", f"{family}:{key}")

    def test_all_renderer_code_reads_canonical_palette(self):
        for renderer in RENDERERS:
            source = next(renderer.glob("piano_*_renderer.py")).read_text(encoding="utf-8")
            self.assertIn("tonality-colors.json", source, renderer.name)
            self.assertIn("load_tonality_colors", source, renderer.name)
            self.assertIn("fill_hex = colors[root][quality]", source, renderer.name)

    def test_all_renderer_docs_point_to_shared_policy_and_runtime_palette(self):
        for renderer in RENDERERS:
            for name in ("README.md", "RENDERER_POLICY.md"):
                text = (renderer / name).read_text(encoding="utf-8")
                self.assertIn("RENDERERS_SOURCE_OF_TRUTH_V1.md", text, f"{renderer.name}/{name}")
                self.assertIn("tonality-colors.json", text, f"{renderer.name}/{name}")

    def test_bootstrap_prioritizes_runtime_palette_before_renderer_docs(self):
        text = POINTER.read_text(encoding="utf-8")
        priority = text.index("## PRIORITÉ ABSOLUE — couleurs et renderers")
        palette = text.index("data/music-theory/tonality-colors.json", priority)
        shared = text.index("docs/chatgpt/RENDERERS_SOURCE_OF_TRUTH_V1.md", priority)
        self.assertLess(palette, shared)

    def test_scale_source_declares_runtime_precedence(self):
        text = (ROOT / "tools" / "piano_scale_renderer" / "SOURCE_IMAGES_GAMMES_PIANO_V1.8.md").read_text(encoding="utf-8")
        self.assertIn("## Statut colorimétrique et priorité", text)
        self.assertIn("data/music-theory/tonality-colors.json", text)
        self.assertIn("RENDERERS_SOURCE_OF_TRUTH_V1.md", text)

    def test_shared_policy_covers_every_renderer(self):
        text = SHARED_POLICY.read_text(encoding="utf-8")
        for renderer in RENDERERS:
            self.assertIn(renderer.name, text)

    def test_no_legacy_red_orange_references_in_renderers(self):
        forbidden = ("#c53650", "#f68c1f", "rouge", "orange")
        for renderer in RENDERERS:
            for path in renderer.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in {".py", ".md", ".json", ".txt"}:
                    continue
                text = path.read_text(encoding="utf-8").lower()
                for token in forbidden:
                    self.assertNotIn(token, text, f"{token} found in {path.relative_to(ROOT)}")

    def test_renderer_unit_tests_resolve_expected_colors_from_runtime_palette(self):
        chord_tests = (ROOT / "tools" / "piano_chord_renderer" / "test_renderer.py").read_text(encoding="utf-8")
        scale_tests = (ROOT / "tools" / "piano_scale_renderer" / "test_renderer.py").read_text(encoding="utf-8")
        pentatonic_tests = (ROOT / "tools" / "piano_scale_renderer" / "test_pentatonic_renderer.py").read_text(encoding="utf-8")
        for text in (chord_tests, scale_tests, pentatonic_tests):
            self.assertIn("tonality-colors.json", text)
            self.assertIn("load_tonality_colors", text)


if __name__ == "__main__":
    unittest.main()
