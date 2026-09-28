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
BLACK = (0, 0, 0)
TEXT = (255, 255, 255)

WHITE_SLOTS = ("C", "D", "E", "F", "G", "A", "B")
BLACK_SLOTS = ("C#", "D#", "F#", "G#", "A#")
ALL_SLOTS = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
EXPECTED_TEMPLATE_SHA256 = "cbda5265b1be6893010e8da73e1b7ab0c25656984724687f2fd13f79f0fa41a9"


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
        result = {}
        for idx, slot in enumerate(WHITE_SLOTS):
            left = self.white_boundaries[idx] + 1
            right = self.white_boundaries[idx + 1] - 1
            result[slot] = (left, self.top + 1, right, self.bottom - 1)
        return result

    @property
    def white_centers(self) -> Dict[str, float]:
        return {
            slot: (self.white_boundaries[i] + self.white_boundaries[i + 1]) / 2
            for i, slot in enumerate(WHITE_SLOTS)
        }

    @property
    def black_centers(self) -> Dict[str, float]:
        return {
            slot: (box[0] + box[2]) / 2
            for slot, box in self.black_boxes.items()
        }


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
        raise ValueError(
            f"Template officiel modifié ou remplacé: sha256={digest}, attendu={EXPECTED_TEMPLATE_SHA256}"
        )


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


def scale_identity(scale_name: str) -> tuple[str, str]:
    root = scale_name.split()[0]
    lower = scale_name.lower()
    if "mineur" in lower:
        quality = "minor"
    elif "majeur" in lower:
        quality = "major"
    else:
        raise ValueError(f"Mode majeur/mineur introuvable dans: {scale_name}")
    return root, quality


def detect_geometry(template: Image.Image) -> Geometry:
    rgb = template.convert("RGB")
    width, height = rgb.size
    nonwhite = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if rgb.getpixel((x, y)) != WHITE
    ]
    if not nonwhite:
        raise ValueError("Template vide ou illisible")

    min_x = min(x for x, _ in nonwhite)
    max_x = max(x for x, _ in nonwhite)
    top = min(y for _, y in nonwhite)
    bottom = max(y for _, y in nonwhite)

    # White-key separators are the tall one-pixel columns spanning the keyboard.
    tall_columns = []
    required = int((bottom - top + 1) * 0.95)
    for x in range(width):
        count = sum(rgb.getpixel((x, y)) != WHITE for y in range(top, bottom + 1))
        if count >= required:
            tall_columns.append(x)
    boundaries = tuple(x for a, b in _runs(tall_columns) for x in ([a] if a == b else [a, b]))
    # In the canonical template each separator is exactly one pixel, yielding 8 boundaries.
    boundaries = tuple(x for x in boundaries if min_x <= x <= max_x)
    if len(boundaries) != 8:
        # Fallback to the canonical documented boundaries; still fail if size is wrong.
        if (width, height) != (365, 254):
            raise ValueError(f"Géométrie inattendue: {width}x{height}, séparateurs={boundaries}")
        boundaries = (10, 59, 108, 157, 206, 255, 304, 353)

    # Black-key boxes are the five wide non-white runs directly below the top border.
    probe_y = top + 1
    probe_runs = [r for r in _runs(x for x in range(width) if rgb.getpixel((x, probe_y)) != WHITE) if r[1] - r[0] >= 10]
    if len(probe_runs) != 5:
        if (width, height) != (365, 254):
            raise ValueError(f"Impossible de détecter les touches noires: {probe_runs}")
        probe_runs = [(42, 77), (91, 126), (188, 223), (237, 272), (286, 321)]

    black_boxes: Dict[str, Tuple[int, int, int, int]] = {}
    for slot, (x1, x2) in zip(BLACK_SLOTS, probe_runs):
        y2 = probe_y
        for y in range(probe_y, bottom):
            if all(rgb.getpixel((x, y)) != WHITE for x in range(x1, x2 + 1)):
                y2 = y
            else:
                break
        black_boxes[slot] = (x1, top, x2, y2)

    geom = Geometry(width, height, top, bottom, boundaries, black_boxes)
    assert_canonical_geometry(geom)
    return geom


def assert_canonical_geometry(geom: Geometry) -> None:
    expected_size = (365, 254)
    expected_boundaries = (10, 59, 108, 157, 206, 255, 304, 353)
    expected_black = {
        "C#": (42, 7, 77, 157),
        "D#": (91, 7, 126, 157),
        "F#": (188, 7, 223, 157),
        "G#": (237, 7, 272, 157),
        "A#": (286, 7, 321, 157),
    }
    if (geom.width, geom.height) != expected_size:
        raise ValueError(f"Template non canonique: {(geom.width, geom.height)} != {expected_size}")
    if geom.white_boundaries != expected_boundaries:
        raise ValueError(f"Séparateurs non canoniques: {geom.white_boundaries}")
    if geom.black_boxes != expected_black:
        raise ValueError(f"Touches noires non canoniques: {geom.black_boxes}")


def find_roboto_condensed_bold() -> Path:
    # Linux / container path first.
    candidates = [
        Path("/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf"),
        Path("/usr/share/fonts/truetype/roboto/RobotoCondensed-Bold.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return path
    try:
        out = subprocess.check_output(
            ["fc-match", "-f", "%{file}", "Roboto Condensed:style=Bold"],
            text=True,
        ).strip()
        if out and Path(out).exists():
            return Path(out)
    except Exception:
        pass
    raise FileNotFoundError(
        "Roboto Condensed Bold introuvable. Installer la police ou utiliser --font /chemin/RobotoCondensed-Bold.ttf"
    )


def _draw_centered_text(draw: ImageDraw.ImageDraw, text: str, center_x: float, visible_bottom: int, font: ImageFont.FreeTypeFont) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    x = round(center_x - width / 2 - bbox[0])
    y = visible_bottom - bbox[3]
    draw.text((x, y), text, fill=TEXT, font=font)


def render_scale(
    template_path: Path,
    notes: Dict[str, str],
    output_path: Path,
    scale_name: str,
    colors_path: Path,
    font_path: Path | None = None,
    validate: bool = True,
) -> dict:
    unknown = set(notes) - set(ALL_SLOTS)
    if unknown:
        raise ValueError(f"Slots inconnus: {sorted(unknown)}")
    if len(notes) != 7:
        raise ValueError(f"Une gamme doit activer exactement 7 slots, reçu: {len(notes)}")

    colors = load_tonality_colors(colors_path)
    root, quality = scale_identity(scale_name)
    if root not in colors:
        raise ValueError(f"Tonique absente de la palette: {root}")
    fill_hex = colors[root][quality]
    fill = hex_to_rgb(fill_hex)

    verify_template_file(template_path)
    template = Image.open(template_path).convert("RGB")
    geom = detect_geometry(template)
    image = template.copy()
    draw = ImageDraw.Draw(image)

    active_white = {slot for slot in notes if slot in WHITE_SLOTS}
    active_black = {slot for slot in notes if slot in BLACK_SLOTS}

    # 1) Fill whole white-key interiors from top to bottom.
    for slot in active_white:
        draw.rectangle(geom.white_boxes[slot], fill=fill)

    # 2) Restore the exact original black-key rectangles from the immutable template.
    for slot, (x1, y1, x2, y2) in geom.black_boxes.items():
        patch = template.crop((x1, y1, x2 + 1, y2 + 1))
        image.paste(patch, (x1, y1))

    draw = ImageDraw.Draw(image)

    # 3) Fill active black keys with the same tonic/mode color.
    # Canonical template rule: keep the original outline and side margins visible.
    for slot in active_black:
        x1, y1, x2, y2 = geom.black_boxes[slot]
        draw.rectangle((x1 + 3, y1 + 1, x2 - 3, y2 - 2), fill=fill)

    # 4) Validate fills BEFORE adding text so labels cannot mask missing color.
    fill_report = validate_fills(image, template, geom, notes, fill) if validate else {"ok": True, "errors": []}
    if validate and not fill_report["ok"]:
        raise AssertionError("Validation des aplats échouée: " + "; ".join(fill_report["errors"]))

    # 5) Add labels with locked font and vertical positions.
    font_path = Path(font_path) if font_path else find_roboto_condensed_bold()
    white_font = ImageFont.truetype(str(font_path), 25)
    black_font = ImageFont.truetype(str(font_path), 20)
    draw = ImageDraw.Draw(image)
    for slot, label in notes.items():
        if slot in WHITE_SLOTS:
            _draw_centered_text(draw, label, geom.white_centers[slot], 216, white_font)
        else:
            _draw_centered_text(draw, label, geom.black_centers[slot], 142, black_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=False)

    final_report = validate_final(image, template, geom, notes, fill_report, fill_hex)
    if validate and not final_report["ok"]:
        output_path.unlink(missing_ok=True)
        raise AssertionError("Validation finale échouée: " + "; ".join(final_report["errors"]))
    return final_report


def _point_in_black_box(x: int, y: int, geom: Geometry) -> bool:
    for x1, y1, x2, y2 in geom.black_boxes.values():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False


def validate_fills(image: Image.Image, template: Image.Image, geom: Geometry, notes: Dict[str, str], fill: tuple[int, int, int]) -> dict:
    errors = []
    rgb = image.convert("RGB")
    active_white = {slot for slot in notes if slot in WHITE_SLOTS}
    active_black = {slot for slot in notes if slot in BLACK_SLOTS}

    # Every visible interior pixel of an active white key must match the scale color before text.
    for slot, (x1, y1, x2, y2) in geom.white_boxes.items():
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if _point_in_black_box(x, y, geom):
                    continue
                pixel = rgb.getpixel((x, y))
                expected = fill if slot in active_white else WHITE
                if pixel != expected:
                    errors.append(f"{slot}: pixel {(x,y)}={pixel}, attendu {expected}")
                    break
            if errors and errors[-1].startswith(slot + ":"):
                break

    # Black-key active color masks are exact and leave the template margins untouched.
    for slot, (x1, y1, x2, y2) in geom.black_boxes.items():
        if slot in active_black:
            for y in range(y1 + 1, y2 - 1):
                for x in range(x1 + 3, x2 - 2):
                    if rgb.getpixel((x, y)) != fill:
                        errors.append(f"{slot}: remplissage couleur incomplet à {(x,y)}")
                        break
                if errors and errors[-1].startswith(slot + ":"):
                    break
            # The preserved margins/outlines must still equal the template.
            if not (errors and errors[-1].startswith(slot + ":")):
                for y in range(y1, y2 + 1):
                    for x in range(x1, x2 + 1):
                        inside_fill = (x1 + 3 <= x <= x2 - 3 and y1 + 1 <= y <= y2 - 2)
                        if inside_fill:
                            continue
                        if rgb.getpixel((x, y)) != template.getpixel((x, y)):
                            errors.append(f"{slot}: marge/contour modifié à {(x,y)}")
                            break
                    if errors and errors[-1].startswith(slot + ":"):
                        break
        else:
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if rgb.getpixel((x, y)) != template.getpixel((x, y)):
                        errors.append(f"{slot}: touche noire inactive modifiée à {(x,y)}")
                        break
                if errors and errors[-1].startswith(slot + ":"):
                    break

    # Structural pixels (outer border, white separators below black keys, black-key outlines) must match template exactly.
    structure_points = []
    for x in range(geom.white_boundaries[0], geom.white_boundaries[-1] + 1):
        structure_points.extend([(x, geom.top), (x, geom.bottom)])
    for x in geom.white_boundaries:
        # White-key separators are allowed to be hidden by a black key above them.
        # Only validate separator pixels that are actually visible in the final template.
        for y in range(geom.top, geom.bottom + 1):
            if any(bx1 <= x <= bx2 and by1 <= y <= by2 for bx1, by1, bx2, by2 in geom.black_boxes.values()):
                continue
            structure_points.append((x, y))
    for x1, y1, x2, y2 in geom.black_boxes.values():
        structure_points.extend((x, y1) for x in range(x1, x2 + 1))
        structure_points.extend((x, y2) for x in range(x1, x2 + 1))
        structure_points.extend((x1, y) for y in range(y1, y2 + 1))
        structure_points.extend((x2, y) for y in range(y1, y2 + 1))
    for point in structure_points:
        if rgb.getpixel(point) != template.getpixel(point):
            errors.append(f"Structure modifiée à {point}")
            break

    return {"ok": not errors, "errors": errors}


def validate_final(image: Image.Image, template: Image.Image, geom: Geometry, notes: Dict[str, str], fill_report: dict, fill_hex: str) -> dict:
    errors = list(fill_report.get("errors", []))
    if image.size != (365, 254):
        errors.append(f"Dimensions finales incorrectes: {image.size}")
    if len(notes) != 7:
        errors.append(f"Nombre de notes actif incorrect: {len(notes)}")

    # Verify each label's theoretical text is non-empty and mapped to one unique physical slot.
    labels = list(notes.values())
    if any(not label.strip() for label in labels):
        errors.append("Libellé vide")
    if len(set(notes.keys())) != 7:
        errors.append("Slots physiques dupliqués")

    return {
        "ok": not errors,
        "errors": errors,
        "size": list(image.size),
        "active_slots": [slot for slot in ALL_SLOTS if slot in notes],
        "labels_by_slot": {slot: notes[slot] for slot in ALL_SLOTS if slot in notes},
        "color": fill_hex,
        "colors": {"active": fill_hex, "text": "#FFFFFF"},
        "template_locked": True,
    }


def load_scales(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Renderer déterministe des gammes piano")
    parser.add_argument("scale", nargs="?", help="Nom de la gamme, ex. 'Db majeur'")
    parser.add_argument("--all", action="store_true", help="Générer toutes les gammes")
    parser.add_argument("--template", type=Path, default=Path(__file__).with_name("official_template.png"))
    parser.add_argument("--scales", type=Path, default=Path(__file__).with_name("scales.json"))
    parser.add_argument("--colors", type=Path, default=Path(__file__).parents[1] / ".." / "data" / "music-theory" / "tonality-colors.json")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("output"))
    parser.add_argument("--font", type=Path, default=None)
    args = parser.parse_args()

    scales = load_scales(args.scales)
    if args.all:
        names = list(scales)
    elif args.scale:
        if args.scale not in scales:
            raise SystemExit(f"Gamme inconnue: {args.scale}\nDisponibles: {', '.join(scales)}")
        names = [args.scale]
    else:
        parser.error("Fournir une gamme ou --all")

    reports = {}
    for name in names:
        cfg = scales[name]
        output = args.output_dir / cfg["filename"]
        reports[name] = render_scale(args.template, cfg["notes"], output, name, args.colors.resolve(), args.font, validate=True)
        print(f"OK  {name} -> {output}")

    report_path = args.output_dir / "validation-report.json"
    report_path.write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rapport: {report_path}")


if __name__ == "__main__":
    main()
