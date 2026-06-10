from __future__ import annotations

import base64
import os
import textwrap
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from app.character_locking import build_character_reference_prompt, create_mock_character_reference_card, save_reference_manifest, slugify_name
from app.continuity import build_full_continuity_prompt_block
from app.schemas import StoryPackage, VideoPrompt

load_dotenv()

IMAGE_SIZE = (1536, 1024)


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


def _gradient_background(size, top=(28, 31, 68), bottom=(235, 199, 158)):
    width, height = size
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(int(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    return img


def create_mock_prompt_image(prompt: VideoPrompt, package: StoryPackage, out_path: Path) -> Path:
    scene = package.scenes[prompt.shot_number - 1]
    storyboard = package.storyboard[prompt.shot_number - 1]

    img = _gradient_background(IMAGE_SIZE, top=(25, 32, 75), bottom=(236, 207, 162)).convert("RGBA")
    img = img.filter(ImageFilter.GaussianBlur(radius=0.2))
    overlay = Image.new("RGBA", IMAGE_SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle((70, 70, 1466, 954), radius=38, fill=(0, 0, 0, 62), outline=(255, 255, 255, 70), width=2)
    d.rounded_rectangle((110, 120, 1426, 540), radius=30, fill=(255, 255, 255, 36))
    d.rounded_rectangle((110, 595, 1426, 900), radius=30, fill=(0, 0, 0, 85))
    for x, y, r in [(170, 110, 90), (1230, 180, 42), (1310, 300, 26), (1180, 780, 24), (220, 810, 16)]:
        d.ellipse((x, y, x + r, y + r), fill=(255, 245, 220, 60))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    title_font = _font(52, bold=True)
    body_font = _font(30)
    meta_font = _font(24)
    small_font = _font(20)

    draw.text((130, 145), f"Generated image placeholder · Shot {prompt.shot_number}", font=meta_font, fill=(255, 230, 180))
    draw.text((130, 190), scene.title, font=title_font, fill=(255, 248, 235))

    y = 265
    for line in textwrap.wrap(storyboard.visual_description, width=58):
        draw.text((130, y), line, font=body_font, fill=(245, 245, 245))
        y += 40

    draw.text((130, 620), "Prompt used", font=meta_font, fill=(255, 235, 190))
    y = 665
    for line in textwrap.wrap(prompt.prompt, width=70):
        draw.text((130, y), line, font=small_font, fill=(245, 242, 236))
        y += 30
        if y > 860:
            break

    draw.text((1110, 900), "Moonlit Showrunner mock visual", font=small_font, fill=(255, 228, 185))
    img.convert("RGB").save(out_path, quality=95)
    return out_path



def build_scene_image_prompt(prompt_text: str, continuity_block: str = "", reference_names: str = "") -> str:
    ref_note = f"Use the approved character reference cards for {reference_names} as the identity anchor. " if reference_names else ""
    return (
        "Create a stylized 3D animated family-film frame, not photorealistic live action. "
        "Use expressive child-friendly character design, rounded forms, soft painterly textures, "
        "warm magical lighting, whimsical storybook atmosphere, cinematic composition, high visual clarity. "
        "Avoid realistic human actors, uncanny faces, horror, harsh realism, and documentary style. "
        "Preserve character identity, costume, proportions, color palette, and environment continuity from the continuity bible. "
        f"{ref_note}{continuity_block} "
        f"Scene prompt: {prompt_text}"
    )


def _names_for_shot(package: StoryPackage, shot_number: int) -> list[str]:
    note = next((n for n in package.shot_continuity_notes if n.shot_number == shot_number), None)
    return note.characters_present if note else []


class OpenAIImageClient:
    def __init__(self, api_key: Optional[str] = None, image_model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.image_model = image_model or os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
        self._client = None
        if self.api_key:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ImportError(
                    "The openai package is required for live image generation. Install dependencies with: "
                    "python -m pip install -r requirements.txt"
                ) from exc
            self._client = OpenAI(api_key=self.api_key)

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key)

    def generate_character_reference_cards(
        self,
        package: StoryPackage,
        output_dir: Path,
        use_mock: bool = False,
        size: str = "1024x1024",
    ) -> Dict[str, Path]:
        refs_dir = output_dir / "character_references"
        refs_dir.mkdir(parents=True, exist_ok=True)

        created: Dict[str, Path] = {}
        for profile in package.character_continuity_profiles:
            slug = slugify_name(profile.name)
            out_path = refs_dir / f"{slug}_reference.png"
            prompt_path = refs_dir / f"{slug}_reference_prompt.txt"
            prompt_text = build_character_reference_prompt(profile, package)
            prompt_path.write_text(prompt_text, encoding="utf-8")

            if use_mock or not self._client:
                create_mock_character_reference_card(profile, out_path)
                created[profile.name] = out_path
                continue

            result = self._client.images.generate(
                model=self.image_model,
                prompt=prompt_text,
                size=size,
            )
            data = result.data[0]
            if getattr(data, "b64_json", None):
                image_bytes = base64.b64decode(data.b64_json)
                out_path.write_bytes(image_bytes)
                created[profile.name] = out_path
            else:
                raise RuntimeError(f"Character reference generation failed for {profile.name}.")

        save_reference_manifest(created, output_dir)
        return created

    def _reference_paths_for_shot(
        self,
        package: StoryPackage,
        shot_number: int,
        character_reference_paths: Optional[Dict[str, Path]] = None,
    ) -> List[Path]:
        if not character_reference_paths:
            return []
        relevant_names = _names_for_shot(package, shot_number)
        return [character_reference_paths[name] for name in relevant_names if name in character_reference_paths]

    def generate_scene_images(
        self,
        package: StoryPackage,
        output_dir: Path,
        use_mock: bool = False,
        size: str = "1536x1024",
        character_reference_paths: Optional[Dict[str, Path]] = None,
    ) -> List[Path]:
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        created: List[Path] = []
        for prompt in package.video_prompts:
            out_path = images_dir / f"shot_{prompt.shot_number:02d}.png"
            if use_mock or not self._client:
                create_mock_prompt_image(prompt, package, out_path)
                created.append(out_path)
                continue

            ref_paths = self._reference_paths_for_shot(package, prompt.shot_number, character_reference_paths)
            ref_names = ", ".join([p.stem.replace("_reference", "").replace("_", " ") for p in ref_paths])
            prompt_text = build_scene_image_prompt(
                prompt.prompt,
                continuity_block=build_full_continuity_prompt_block(package, prompt.shot_number),
                reference_names=ref_names,
            )
            prompt_file = images_dir / f"shot_{prompt.shot_number:02d}_prompt.txt"
            prompt_file.write_text(prompt_text, encoding="utf-8")

            result = None
            if ref_paths and hasattr(self._client.images, "edit"):
                files = [open(path, "rb") for path in ref_paths]
                try:
                    result = self._client.images.edit(
                        model=self.image_model,
                        image=files,
                        prompt=prompt_text,
                        size=size,
                    )
                except Exception:
                    result = self._client.images.generate(
                        model=self.image_model,
                        prompt=prompt_text,
                        size=size,
                    )
                finally:
                    for f in files:
                        try:
                            f.close()
                        except Exception:
                            pass
            else:
                result = self._client.images.generate(
                    model=self.image_model,
                    prompt=prompt_text,
                    size=size,
                )

            data = result.data[0]
            if getattr(data, "b64_json", None):
                image_bytes = base64.b64decode(data.b64_json)
                out_path.write_bytes(image_bytes)
                created.append(out_path)
            else:
                raise RuntimeError("Image generation did not return base64 image data.")

        return created
