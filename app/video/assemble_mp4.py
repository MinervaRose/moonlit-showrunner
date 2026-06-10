from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from app.schemas import StoryPackage
from app.video.make_cards import create_scene_card, create_scene_frame_from_image, create_title_card


def _find_generated_image_map(output_dir: Path) -> Dict[int, Path]:
    images_dir = output_dir / "images"
    mapping: Dict[int, Path] = {}
    if not images_dir.exists():
        return mapping
    for path in sorted(images_dir.glob("shot_*.png")):
        try:
            number = int(path.stem.split("_")[-1])
            mapping[number] = path
        except Exception:
            continue
    return mapping


def assemble_story_video(package: StoryPackage, output_dir: Path, use_generated_images: bool = True) -> Path:
    """Create an MP4 from a title card plus either generated scene images or fallback scene cards."""
    output_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    generated_image_map = _find_generated_image_map(output_dir) if use_generated_images else {}

    title_path = create_title_card(package, frames_dir / "00_title.jpg")
    card_paths: list[Path] = [title_path]
    durations: list[int] = [4]

    edits_by_scene = {e.scene_number: e for e in package.edit_decisions}
    for idx, scene in enumerate(package.scenes, start=1):
        edit = edits_by_scene.get(scene.scene_number)
        if edit is None:
            from app.schemas import EditDecision
            edit = EditDecision(
                order=idx,
                scene_number=scene.scene_number,
                shot_number=idx,
                duration_seconds=scene.duration_seconds,
                on_screen_text=scene.dialogue_or_caption,
                transition="cut",
                audio_note=scene.sound_or_music_notes,
            )

        out_frame = frames_dir / f"{idx:02d}_scene_{scene.scene_number}.jpg"
        source_img = generated_image_map.get(idx)
        if source_img and source_img.exists():
            path = create_scene_frame_from_image(source_img, scene, edit, out_frame)
        else:
            path = create_scene_card(scene, edit, out_frame, palette_index=idx)

        card_paths.append(path)
        durations.append(edit.duration_seconds)

    video_path = output_dir / "moonlit_showrunner_animatic.mp4"

    try:
        try:
            from moviepy.editor import ImageClip, concatenate_videoclips
        except Exception:
            from moviepy import ImageClip, concatenate_videoclips

        clips = []
        for path, duration in zip(card_paths, durations):
            clip = ImageClip(str(path))
            if hasattr(clip, "set_duration"):
                clip = clip.set_duration(duration)
            else:
                clip = clip.with_duration(duration)
            clips.append(clip)

        final = concatenate_videoclips(clips, method="compose")
        try:
            final.write_videofile(str(video_path), fps=24, codec="libx264", audio=False, verbose=False, logger=None)
        except TypeError:
            final.write_videofile(str(video_path), fps=24, codec="libx264", audio=False, logger=None)
        final.close()
        for clip in clips:
            clip.close()
    except Exception as exc:
        manifest = output_dir / "video_fallback_manifest.txt"
        manifest.write_text(
            "MoviePy video assembly failed. Generated frames are available here:\n"
            + "\n".join(str(p) for p in card_paths)
            + f"\n\nError: {exc}\n",
            encoding="utf-8",
        )
        raise RuntimeError(f"MP4 assembly failed. See {manifest}") from exc

    return video_path
