from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from app.openai_client import OpenAIStoryClient
from app.schemas import StoryPackage
from app.video.assemble_mp4 import assemble_story_video


DEFAULT_OUTPUT_DIR = Path("outputs")


class MoonlitPipeline:
    def __init__(self, model: Optional[str] = None):
        self.client = OpenAIStoryClient(model=model)

    def generate(self, premise: str, use_mock: bool = False) -> StoryPackage:
        return self.client.generate_story_package(premise=premise, use_mock=use_mock)

    def save_package(self, package: StoryPackage, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict[str, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "story_package.json"
        md_path = output_dir / "story_package.md"
        json_path.write_text(package.model_dump_json(indent=2), encoding="utf-8")
        md_path.write_text(package.to_markdown(), encoding="utf-8")
        return {"json": json_path, "markdown": md_path}

    def create_video(self, package: StoryPackage, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        return assemble_story_video(package, output_dir=output_dir)


def run_full_pipeline(premise: str, use_mock: bool = False, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict:
    pipeline = MoonlitPipeline()
    package = pipeline.generate(premise=premise, use_mock=use_mock)
    saved = pipeline.save_package(package, output_dir=output_dir)
    video_path = pipeline.create_video(package, output_dir=output_dir)
    return {"package": package, "files": saved, "video": video_path}
