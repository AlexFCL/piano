from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)
TEXT = (255, 255, 255)
EXPECTED_TEMPLATE_SHA256 = "4f395f36d61d0eb9e350db97081a24fc45a8fd3cf8dbd714a0e5bd94aba8f422"

WHITE_SLOTS = ("C1", "D1", "E1", "F1", "G1", "A1", "B1", "C2", "D2", "E2", "F2", "G2", "A2", "B2")
BLACK_SLOTS = ("C#1", "D#1", "F#1", "G#1", "A#1", "C#2", "D#2", "F#2", "G#2", "A#2")
ALL_SLOTS = (
    "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
    "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
)
ROOT_ORDER = ("C", "D", "E", "F", "G", "A", "B", "C#", "Db", "D#", "Eb", "F#", "Gb", "G#", "Ab", "A#", "Bb")
LETTERS = ("C", "D", "E", "F", "G", "A", "B")
NATURAL_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


@dataclass(frozen=True)
class Geometry:
    width: int
    height: int
    top: int
    bottom: int
    white_boundaries: Tuple[int, ...]
    black_boxes: Dict[str, Tuple[int, int, int, int]]

    @property
    def white_boxes(self) -> Dict[str, Tuple[int, int, int, int]]:
        out = {}
        for i, slot in enumerate(WHITE_SLOTS):
            out[slot] = (
                self.white_boundaries[i] + 1,
                self.top + 1,
                self.white_boundaries[i + 1] - 1,
                self.bottom - 1,
            )
        return out

    @property
    def white_centers(self) -> Dict[str, float]:
        return {
            slot: (self.white_boundaries[i] + self.white_boundaries[i + 1]) / 2
            for i, slot in enumerate(WHITE_SLOTS)
        }

    @property
    def black_centers(self) -> Dict[str, float]:
        return {slot: (box[0] + box[2]) / 2 for slot, box in self.black_boxes.items()}


def _runs(values: Iterable[int]) -> list[tuple[int, int]]:
    vals = sorted(values)
    if not vals:
        return []
    out = []
    start = prev = vals[0]
    for value in vals[1:]:
        if value == prev + 1:
            prev = value
        else:
            out.append((start, prev))
            start = prev = value
    out.append((start, prev))
    return out


def verify_template_file(path: Path) -> None:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != EXPECTED_TEMPLATE_SHA256:
        raise ValueError(f"Template accords modifié: {digest} != {EXPECTED_TEMPLATE_SHA256}")


def detect_geometry(template: Image.Image) -> Geometry:
    rgb = template.convert("RGB")
    width, height = rgb.size
    if (width, height) != (711, 254):
        raise ValueError(f"Format template accords inattendu: {(width, height)}")

    nonwhite = [(x, y) for y in range(height) for x in range(width) if rgb.getpixel((x, y)) != WHITE]
    top = min(y for _, y in nonwhite)
    bottom = max(y for _, y in nonwhite)
    min_x = min(x for x, _ in nonwhite)
    max_x = max(x for x, _ in nonwhite)

    required = int((bottom - top + 1) * 0.95)
    tall_columns = []
    for x in range(width):
        count = sum(rgb.getpixel((x, y)) != WHITE for y in range(top, bottom + 1))
        if count >= required:
            tall_columns.append(x)
    boundaries = tuple(x for a, b in _runs(tall_columns) for x in ([a] if a == b else [a, b]))
    boundaries = tuple(x for x in boundaries if min_x <= x <= max_x)
    expected = (14, 63, 112, 161, 210, 259, 308, 357, 406, 455, 504, 553, 602, 651, 700)
    if boundaries != expected:
        raise ValueError(f"Séparateurs accords non canoniques: {boundaries}")

    probe_y = top + 1
    probe_runs = [
        r for r in _runs(x for x in range(width) if rgb.getpixel((x, probe_y)) != WHITE)
        if r[1] - r[0] >= 30
    ]
    expected_runs = (
        (46, 81), (95, 130), (192, 227), (241, 276), (290, 325),
        (389, 424), (438, 473), (535, 570), (584, 619), (633, 668),
    )
    if tuple(probe_runs) != expected_runs:
        raise ValueError(f"Touches noires accords non canoniques: {probe_runs}")

    black_boxes = {}
    for slot, (x1, x2) in zip(BLACK_SLOTS, probe_runs):
        y2 = probe_y
        for y in range(probe_y, bottom):
            if all(rgb.getpixel((x, y)) != WHITE for x in range(x1, x2 + 1)):
                y2 = y
            else:
                break
        black_boxes[slot] = (x1, top, x2, y2)
    return Geometry(width, height, top, bottom, boundaries, black_boxes)


def note_to_pc(note: str) -> int:
    pc = NATURAL_PC[note[0]]
    for accidental in note[1:]:
        if accidental == "#":
            pc += 1
        elif accidental == "b":
            pc -= 1
        else:
            raise ValueError(f"Note non reconnue: {note}")
    return pc % 12


def _spell_interval(root: str, diatonic_steps: int, semitones: int) -> str:
    target_letter = LETTERS[(LETTERS.index(root[0]) + diatonic_steps) % 7]
    target_pc = (note_to_pc(root) + semitones) % 12
    delta = target_pc - NATURAL_PC[target_letter]
    while delta <= -6:
        delta += 12
    while delta > 6:
        delta -= 12
    if abs(delta) > 2:
        raise ValueError(f"Orthographe théorique inhabituelle pour {root}: {target_letter}, delta={delta}")
    return target_letter + ("#" * delta if delta > 0 else "b" * (-delta))


def triad_labels(root: str, quality: str) -> list[str]:
    if quality == "major":
        return [root, _spell_interval(root, 2, 4), _spell_interval(root, 4, 7)]
    if quality == "minor":
        return [root, _spell_interval(root, 2, 3), _spell_interval(root, 4, 7)]
    raise ValueError(f"Qualité inconnue: {quality}")


def _ordered_for_inversion(labels: list[str], inversion: int) -> list[str]:
    if inversion == 0:
        return labels
    if inversion == 1:
        return [labels[1], labels[2], labels[0]]
    if inversion == 2:
        return [labels[2], labels[0], labels[1]]
    raise ValueError(f"Renversement inconnu: {inversion}")


def choose_slots(labels: list[str], inversion: int) -> list[str]:
    ordered = _ordered_for_inversion(labels, inversion)
    pcs = [note_to_pc(note) for note in ordered]
    candidates = []
    for first_octave in (0, 12):
        pitches = [pcs[0] + first_octave]
        for pc in pcs[1:]:
            pitch = pc
            while pitch <= pitches[-1]:
                pitch += 12
            pitches.append(pitch)
        if min(pitches) >= 0 and max(pitches) <= 23:
            candidates.append((abs(sum(pitches) / 3 - 14.5), pitches))
    if not candidates:
        raise ValueError(f"Aucun voicing sur deux octaves pour {labels}, inversion {inversion}")
    candidates.sort(key=lambda item: item[0])
    return [ALL_SLOTS[pitch] for pitch in candidates[0][1]]


def load_tonality_colors(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    aliases = {}
    for family, cfg in data.items():
        for alias in cfg["aliases"]:
            aliases[alias] = {"family": family, **cfg}
    return aliases


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def find_roboto_condensed_bold() -> Path:
    candidates = [
        Path("/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"),
        Path("/usr/share/fonts/truetype/roboto/RobotoCondensed-Bold.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return path
    out = subprocess.check_output(
        ["fc-match", "-f", "%{file}", "Roboto Condensed:style=Bold"], text=True
    ).strip()
    if out and Path(out).exists():
        return Path(out)
    raise FileNotFoundError("Roboto Condensed Bold introuvable")


def _draw_centered_text(draw, text, center_x, visible_bottom, font) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    x = round(center_x - width / 2 - bbox[0])
    y = visible_bottom - bbox[3]
    draw.text((x, y), text, fill=TEXT, font=font)


def render_chord(template_path: Path, colors_path: Path, root: str, quality: str, inversion: int,
                 output_path: Path, font_path: Path | None = None) -> dict:
    verify_template_file(template_path)
    template = Image.open(template_path).convert("RGB")
    geom = detect_geometry(template)
    colors = load_tonality_colors(colors_path)
    if root not in colors:
        raise ValueError(f"Tonique absente de la palette: {root}")

    labels = triad_labels(root, quality)
    slots = choose_slots(labels, inversion)
    ordered_labels = _ordered_for_inversion(labels, inversion)
    label_by_slot = dict(zip(slots, ordered_labels))
    fill_hex = colors[root][quality]
    fill = hex_to_rgb(fill_hex)

    image = template.copy()
    draw = ImageDraw.Draw(image)
    for slot in slots:
        if slot in geom.white_boxes:
            draw.rectangle(geom.white_boxes[slot], fill=fill)

    for slot, (x1, y1, x2, y2) in geom.black_boxes.items():
        image.paste(template.crop((x1, y1, x2 + 1, y2 + 1)), (x1, y1))

    draw = ImageDraw.Draw(image)
    for slot in slots:
        if slot in geom.black_boxes:
            x1, y1, x2, y2 = geom.black_boxes[slot]
            draw.rectangle((x1 + 3, y1 + 1, x2 - 3, y2 - 2), fill=fill)

    font_path = Path(font_path) if font_path else find_roboto_condensed_bold()
    white_font = ImageFont.truetype(str(font_path), 24)
    black_font = ImageFont.truetype(str(font_path), 19)
    draw = ImageDraw.Draw(image)
    for slot, label in label_by_slot.items():
        if slot in geom.white_boxes:
            _draw_centered_text(draw, label, geom.white_centers[slot], 216, white_font)
        else:
            _draw_centered_text(draw, label, geom.black_centers[slot], 142, black_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=False)

    return {
        "ok": True,
        "root": root,
        "quality": quality,
        "inversion": inversion,
        "color": fill_hex,
        "family": colors[root]["family"],
        "labels": ordered_labels,
        "active_slots": slots,
        "labels_by_slot": label_by_slot,
        "size": list(image.size),
        "template_locked": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Renderer déterministe des accords piano")
    parser.add_argument("root", choices=ROOT_ORDER)
    parser.add_argument("quality", choices=("major", "minor"))
    parser.add_argument("inversion", type=int, choices=(0, 1, 2))
    parser.add_argument("--template", type=Path, default=Path(__file__).with_name("official_template.png"))
    parser.add_argument("--colors", type=Path, default=Path(__file__).parents[1] / ".." / "data" / "music-theory" / "tonality-colors.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("output") / "chord.png")
    parser.add_argument("--font", type=Path, default=None)
    args = parser.parse_args()
    report = render_chord(args.template, args.colors.resolve(), args.root, args.quality, args.inversion, args.output, args.font)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
