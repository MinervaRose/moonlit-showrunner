from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from app.schemas import EditDecision, Scene, StoryPackage

SIZE = (1280, 720)


def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _gradient_background(size: Tuple[int, int], top=(28, 31, 68), bottom=(247, 210, 150)) -> Image.Image:
    width, height = size
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(int(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    return img


def _draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: Tuple[int, int], font, fill, width_chars: int, line_spacing: int = 10):
    x, y = xy
    for line in textwrap.wrap(text, width=width_chars):
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def create_title_card(package: StoryPackage, out_path: Path) -> Path:
    img = _gradient_background(SIZE, top=(18, 20, 52), bottom=(151, 125, 185))
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((90, 100, 1190, 620), radius=36, fill=(255, 255, 255, 34), outline=(255,255,255,120), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    title_font = _font(72, bold=True)
    sub_font = _font(30)
    small_font = _font(24)
    draw.text((140, 180), package.brief.title, font=title_font, fill=(255, 248, 230))
    _draw_wrapped(draw, package.brief.logline, (145, 300), sub_font, (255, 244, 220), width_chars=58, line_spacing=12)
    draw.text((145, 520), "Moonlit Showrunner · AI short-drama prototype", font=small_font, fill=(255, 235, 190))
    img.convert("RGB").save(out_path, quality=95)
    return out_path


def create_scene_card(scene: Scene, edit: EditDecision, out_path: Path, palette_index: int = 0) -> Path:
    palettes = [
        ((18, 20, 52), (145, 130, 190)),
        ((20, 35, 70), (190, 170, 220)),
        ((28, 31, 68), (210, 180, 130)),
        ((26, 40, 70), (120, 95, 160)),
        ((72, 50, 76), (244, 196, 126)),
        ((35, 38, 60), (255, 210, 150)),
    ]
    top, bottom = palettes[palette_index % len(palettes)]
    img = _gradient_background(SIZE, top=top, bottom=bottom).convert("RGBA")
    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((80, 70, 1200, 650), radius=32, fill=(0, 0, 0, 70), outline=(255, 255, 255, 80), width=2)
    # Decorative moon/star shapes
    d.ellipse((1020, 105, 1100, 185), fill=(255, 245, 210, 160))
    for x, y in [(180,120), (1120,260), (980,500), (250,570), (620,130)]:
        d.ellipse((x, y, x+5, y+5), fill=(255, 245, 220, 180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    small = _font(24)
    title = _font(50, bold=True)
    body = _font(31)
    caption = _font(36, bold=True)
    draw.text((120, 105), f"Scene {scene.scene_number}", font=small, fill=(255, 226, 170))
    draw.text((120, 145), scene.title, font=title, fill=(255, 248, 230))
    y = _draw_wrapped(draw, scene.action, (120, 235), body, (245, 242, 235), width_chars=72, line_spacing=10)
    draw.line((120, y+18, 1160, y+18), fill=(255,255,255,90), width=1)
    _draw_wrapped(draw, edit.on_screen_text, (120, y+48), caption, (255, 240, 190), width_chars=54, line_spacing=12)
    draw.text((120, 595), f"Camera: {scene.camera_direction}", font=small, fill=(230, 230, 240))
    img.convert("RGB").save(out_path, quality=95)
    return out_path
