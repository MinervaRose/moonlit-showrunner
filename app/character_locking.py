from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from typing import Dict

from PIL import Image, ImageDraw, ImageFilter

from app.schemas import CharacterContinuityProfile, StoryPackage


def slugify_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return slug or "character"


def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for c in candidates:
        try:
            from PIL import ImageFont
            return ImageFont.truetype(c, size=size)
        except Exception:
            continue
    from PIL import ImageFont
    return ImageFont.load_default()


def build_character_reference_prompt(profile: CharacterContinuityProfile, package: StoryPackage) -> str:
    style = package.visual_style_bible
    return (
        "Create a polished character reference card for a stylized 3D animated family-film project. "
        "Show a full-body hero pose with clear face visibility, consistent clothing, and a clean neutral presentation that can be reused as a character identity anchor. "
        "Do not make the image photorealistic. Keep it storybook-like, child-friendly, and highly legible. "
        f"Character: {profile.name}. "
        f"Stable identity: {profile.stable_identity}. "
        f"Face/body: {profile.face_and_body}. "
        f"Hair/eyes: {profile.hair_and_eyes}. "
        f"Clothing/props: {profile.clothing_and_props}. "
        f"Expression/movement: {profile.expression_and_movement}. "
        f"Do not change: {'; '.join(profile.do_not_change)}. "
        f"Overall style: {style.overall_style}. "
        f"Color palette: {style.color_palette}. "
        f"Lighting rules: {style.lighting_rules}. "
        "Use a simple attractive reference-card composition. No logos, no readable decorative text beyond the character name if needed."
    )


def create_mock_character_reference_card(profile: CharacterContinuityProfile, out_path: Path) -> Path:
    size = (1024, 1024)
    bg = Image.new('RGB', size, (37, 44, 92))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=0.2))
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle((50, 50, 974, 974), radius=40, fill=(250, 245, 237), outline=(190, 180, 210), width=3)
    draw.rounded_rectangle((100, 115, 924, 550), radius=28, fill=(218, 228, 245))
    draw.rounded_rectangle((100, 590, 924, 920), radius=28, fill=(245, 240, 235))

    title_font = _font(42, bold=True)
    body_font = _font(28)
    small_font = _font(22)

    # character silhouette placeholder
    draw.ellipse((370, 165, 655, 450), fill=(240, 222, 200), outline=(150, 130, 120), width=3)
    draw.rounded_rectangle((425, 420, 600, 710), radius=24, fill=(160, 180, 225), outline=(110, 120, 170), width=3)
    draw.line((470, 710, 440, 850), fill=(120, 110, 120), width=8)
    draw.line((555, 710, 585, 850), fill=(120, 110, 120), width=8)
    draw.line((420, 520, 335, 640), fill=(120, 110, 120), width=8)
    draw.line((605, 520, 690, 640), fill=(120, 110, 120), width=8)

    draw.text((120, 70), f"Character lock · {profile.name}", font=title_font, fill=(54, 62, 103))
    y = 620
    for label, value in [
        ('Identity', profile.stable_identity),
        ('Face/body', profile.face_and_body),
        ('Hair/eyes', profile.hair_and_eyes),
        ('Clothing/props', profile.clothing_and_props),
    ]:
        draw.text((125, y), f"{label}:", font=body_font, fill=(70, 76, 104))
        y += 36
        for line in textwrap.wrap(value, width=54):
            draw.text((145, y), line, font=small_font, fill=(80, 80, 88))
            y += 26
        y += 8

    out_path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, quality=95)
    return out_path


def save_reference_manifest(reference_paths: Dict[str, Path], output_dir: Path) -> Path:
    manifest = {name: str(path) for name, path in reference_paths.items()}
    out = output_dir / 'character_references' / 'reference_manifest.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return out
