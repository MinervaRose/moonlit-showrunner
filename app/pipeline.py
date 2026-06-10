from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from app.image_client import OpenAIImageClient
from app.openai_client import OpenAIStoryClient
from app.sora_client import SoraVideoClient, build_sora_prompt_for_shot, concatenate_sora_clips
from app.schemas import StoryPackage
from app.video.assemble_mp4 import assemble_story_video

DEFAULT_OUTPUT_ROOT = Path("outputs")
DEFAULT_RUNS_DIR = DEFAULT_OUTPUT_ROOT / "runs"


class MoonlitPipeline:
    def __init__(self, model: Optional[str] = None, image_model: Optional[str] = None, video_model: Optional[str] = None):
        self.client = OpenAIStoryClient(model=model)
        self.image_client = OpenAIImageClient(image_model=image_model)
        self.video_client = SoraVideoClient(model=video_model)

    def create_run_dir(self, root_dir: Path = DEFAULT_RUNS_DIR) -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        run_dir = root_dir / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def generate(self, premise: str, use_mock: bool = False) -> StoryPackage:
        return self.client.generate_story_package(premise=premise, use_mock=use_mock)

    def save_package(self, package: StoryPackage, output_dir: Path) -> dict[str, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "story_package.json"
        md_path = output_dir / "story_package.md"
        json_path.write_text(package.model_dump_json(indent=2), encoding="utf-8")
        md_path.write_text(package.to_markdown(), encoding="utf-8")
        return {"json": json_path, "markdown": md_path}

    def generate_character_references(self, package: StoryPackage, output_dir: Path, use_mock: bool = False) -> dict[str, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        return self.image_client.generate_character_reference_cards(package=package, output_dir=output_dir, use_mock=use_mock)

    def generate_images(self, package: StoryPackage, output_dir: Path, use_mock: bool = False, character_reference_paths: Optional[dict[str, Path]] = None) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        return self.image_client.generate_scene_images(package=package, output_dir=output_dir, use_mock=use_mock, character_reference_paths=character_reference_paths)


    def create_sora_prompt(self, package: StoryPackage, shot_number: int = 1) -> str:
        return build_sora_prompt_for_shot(package=package, shot_number=shot_number)

    def generate_real_video_clip(
        self,
        package: StoryPackage,
        output_dir: Path,
        shot_number: int = 1,
        model: Optional[str] = None,
        size: str = "1280x720",
        seconds: str = "4",
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        prompt = self.create_sora_prompt(package=package, shot_number=shot_number)
        return self.video_client.generate_video_clip(
            prompt=prompt,
            output_dir=output_dir,
            model=model,
            size=size,
            seconds=seconds,
        )


    def generate_full_real_video(
        self,
        package: StoryPackage,
        output_dir: Path,
        model: Optional[str] = None,
        size: str = "1280x720",
        seconds_per_clip: str = "4",
        max_shots: Optional[int] = None,
    ) -> dict[str, object]:
        """Generate one real Sora clip per shot and concatenate them into a full MP4."""
        output_dir.mkdir(parents=True, exist_ok=True)
        clips = self.video_client.generate_all_video_clips(
            package=package,
            output_dir=output_dir,
            model=model,
            size=size,
            seconds=seconds_per_clip,
            max_shots=max_shots,
        )
        full_video = concatenate_sora_clips(clips, output_dir=output_dir)
        return {"clips": clips, "full_video": full_video}

    def create_video(self, package: StoryPackage, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        return assemble_story_video(package, output_dir=output_dir, use_generated_images=True)


def run_full_pipeline(premise: str, use_mock: bool = False, output_dir: Optional[Path] = None) -> dict:
    pipeline = MoonlitPipeline()
    actual_output_dir = output_dir or pipeline.create_run_dir()
    package = pipeline.generate(premise=premise, use_mock=use_mock)
    saved = pipeline.save_package(package, output_dir=actual_output_dir)
    refs = pipeline.generate_character_references(package, output_dir=actual_output_dir, use_mock=use_mock)
    images = pipeline.generate_images(package, output_dir=actual_output_dir, use_mock=use_mock, character_reference_paths=refs)
    video_path = pipeline.create_video(package, output_dir=actual_output_dir)
    return {"package": package, "files": saved, "images": images, "video": video_path, "run_dir": actual_output_dir}
