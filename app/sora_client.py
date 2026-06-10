from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional, List

from dotenv import load_dotenv

from app.schemas import StoryPackage

load_dotenv()


def build_sora_prompt_for_shot(package: StoryPackage, shot_number: int) -> str:
    """Build a compact Sora-ready prompt from the story package and selected shot."""
    shot = next((s for s in package.storyboard if s.shot_number == shot_number), None)
    scene = next((s for s in package.scenes if s.scene_number == shot_number), None)
    video_prompt = next((p for p in package.video_prompts if p.shot_number == shot_number), None)

    if not shot or not scene or not video_prompt:
        raise ValueError(f"Could not find complete shot data for shot {shot_number}.")

    return (
        "Create a short stylized 3D animated family-film video clip, not photorealistic live action. "
        "Use expressive child-friendly character design, rounded forms, soft painterly textures, "
        "warm magical lighting, whimsical storybook atmosphere, cinematic composition, and gentle motion. "
        "Avoid realistic human actors, uncanny faces, horror, harsh realism, documentary style, copyrighted characters, and copyrighted music. "
        f"Story title: {package.brief.title}. "
        f"Scene: {scene.title}. "
        f"Action: {scene.action}. "
        f"Emotional beat: {scene.emotional_beat}. "
        f"Camera direction: {scene.camera_direction}. "
        f"Shot type: {shot.shot_type}. "
        f"Visual description: {shot.visual_description}. "
        f"Camera movement: {shot.camera_movement}. "
        f"Lighting: {shot.lighting}. "
        f"Prompt detail: {video_prompt.prompt}. "
        "No readable text, no subtitles, no logos, no watermarks."
    )


class SoraVideoClient:
    """Small wrapper around OpenAI's Videos API.

    The Videos API is asynchronous: a render job is created, polled, then the final MP4 is downloaded.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_VIDEO_MODEL", "sora-2")
        self._client = None

        if self.api_key:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ImportError(
                    "The openai package is required for live video generation. Install dependencies with: "
                    "python -m pip install -r requirements.txt"
                ) from exc
            self._client = OpenAI(api_key=self.api_key)

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key)

    def generate_video_clip(
        self,
        prompt: str,
        output_dir: Path,
        model: Optional[str] = None,
        size: str = "1280x720",
        seconds: str = "4",
        poll_interval_seconds: int = 10,
        max_wait_minutes: int = 30,
    ) -> Path:
        if not self._client:
            raise RuntimeError("No OpenAI API key found. Add OPENAI_API_KEY to .streamlit/secrets.toml or use mock mode.")

        output_dir.mkdir(parents=True, exist_ok=True)
        video_dir = output_dir / "sora_video"
        video_dir.mkdir(parents=True, exist_ok=True)

        prompt_path = video_dir / "sora_prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")

        selected_model = model or self.model

        if not hasattr(self._client, "videos"):
            raise RuntimeError(
                "This installed openai package does not expose the Videos API. "
                "Upgrade with: .venv\\Scripts\\python.exe -m pip install --upgrade openai"
            )

        video = self._client.videos.create(
            model=selected_model,
            prompt=prompt,
            size=size,
            seconds=seconds,
        )

        started = time.time()
        while getattr(video, "status", None) in ("queued", "in_progress"):
            elapsed = time.time() - started
            if elapsed > max_wait_minutes * 60:
                raise TimeoutError(f"Sora video generation timed out after {max_wait_minutes} minutes.")

            time.sleep(poll_interval_seconds)
            video = self._client.videos.retrieve(video.id)

        if getattr(video, "status", None) != "completed":
            error = getattr(video, "error", None)
            message = getattr(error, "message", None) if error else None
            raise RuntimeError(f"Sora video generation failed. Status: {getattr(video, 'status', None)}. {message or ''}")

        out_path = video_dir / f"{video.id}.mp4"
        content = self._client.videos.download_content(video.id, variant="video")
        content.write_to_file(str(out_path))

        metadata_path = video_dir / "sora_video_metadata.txt"
        metadata_path.write_text(
            f"video_id={video.id}\n"
            f"model={selected_model}\n"
            f"size={size}\n"
            f"seconds={seconds}\n"
            f"status={getattr(video, 'status', None)}\n"
            f"output={out_path}\n",
            encoding="utf-8",
        )

        return out_path


    def generate_all_video_clips(
        self,
        package: StoryPackage,
        output_dir: Path,
        model: Optional[str] = None,
        size: str = "1280x720",
        seconds: str = "4",
        max_shots: Optional[int] = None,
        poll_interval_seconds: int = 10,
        max_wait_minutes_per_clip: int = 30,
    ) -> List[Path]:
        """Generate one Sora MP4 clip for each storyboard shot.

        This is intentionally sequential for safety and easier debugging.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        video_dir = output_dir / "sora_video"
        video_dir.mkdir(parents=True, exist_ok=True)

        shot_numbers = [p.shot_number for p in package.video_prompts]
        shot_numbers = sorted(set(shot_numbers))
        if max_shots is not None:
            shot_numbers = shot_numbers[:max_shots]

        created: List[Path] = []
        prompts_manifest = []

        for shot_number in shot_numbers:
            prompt = build_sora_prompt_for_shot(package, shot_number=shot_number)
            shot_prompt_path = video_dir / f"sora_prompt_shot_{shot_number:02d}.txt"
            shot_prompt_path.write_text(prompt, encoding="utf-8")
            prompts_manifest.append(f"Shot {shot_number}: {shot_prompt_path}")

            path = self.generate_video_clip(
                prompt=prompt,
                output_dir=output_dir,
                model=model,
                size=size,
                seconds=seconds,
                poll_interval_seconds=poll_interval_seconds,
                max_wait_minutes=max_wait_minutes_per_clip,
            )

            # Copy/rename the downloaded file to a stable shot-based name.
            stable_path = video_dir / f"shot_{shot_number:02d}_sora.mp4"
            if path != stable_path:
                stable_path.write_bytes(path.read_bytes())
            created.append(stable_path)

        (video_dir / "sora_prompts_manifest.txt").write_text("\n".join(prompts_manifest), encoding="utf-8")
        return created


def concatenate_sora_clips(clip_paths: List[Path], output_dir: Path) -> Path:
    """Concatenate Sora-generated clips into a full real-video MP4."""
    if not clip_paths:
        raise ValueError("No Sora clips were provided for concatenation.")

    output_dir.mkdir(parents=True, exist_ok=True)
    video_dir = output_dir / "sora_video"
    video_dir.mkdir(parents=True, exist_ok=True)
    out_path = video_dir / "moonlit_showrunner_full_sora_video.mp4"

    try:
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
        except Exception:
            from moviepy import VideoFileClip, concatenate_videoclips

        clips = [VideoFileClip(str(path)) for path in clip_paths]
        final = concatenate_videoclips(clips, method="compose")
        try:
            final.write_videofile(str(out_path), fps=24, codec="libx264", audio=False, verbose=False, logger=None)
        except TypeError:
            final.write_videofile(str(out_path), fps=24, codec="libx264", audio=False, logger=None)
        final.close()
        for clip in clips:
            clip.close()

    except Exception as exc:
        manifest = video_dir / "full_video_fallback_manifest.txt"
        manifest.write_text(
            "Sora clip concatenation failed. Individual clips are available here:\n"
            + "\n".join(str(p) for p in clip_paths)
            + f"\n\nError: {exc}\n",
            encoding="utf-8",
        )
        raise RuntimeError(f"Full Sora video assembly failed. See {manifest}") from exc

    return out_path
