from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from app.sample_data import get_sample_story_package
from app.schemas import StoryPackage

load_dotenv()

SYSTEM_PROMPT = """You are Moonlit Showrunner, an AI creative production pipeline.
You transform a short premise into a coherent, emotionally satisfying short-drama production package.
You must optimize for clear visual storytelling, low dialogue, strong emotional arc, practical MP4 assembly,
and strong shot-to-shot character continuity.
The visual direction should favor a stylized 3D family-animation look: expressive characters, rounded forms,
warm magical lighting, storybook color palettes, soft cinematic depth, and charming non-photorealistic design.
Avoid realistic live-action human actor aesthetics unless the user explicitly asks for them.
Return only valid JSON matching the provided schema.
"""

USER_PROMPT_TEMPLATE = """Create a complete short-drama production package from this premise:

{premise}

Constraints:
- Duration: 30 to 60 seconds.
- Exactly 6 scenes.
- Exactly 6 storyboard shots, one primary shot per scene.
- Family-friendly, magical or emotional tone.
- Minimal dialogue; prefer captions and visual storytelling.
- Each video prompt must be usable for image generation and future video generation.
- Create a Character Continuity Bible for all recurring characters.
- Create a Global Continuity Lock that can be prepended to all image and Sora prompts.
- Create one Shot Continuity Note per storyboard shot, carrying forward character state, costume, props, environment, and continuity risks.
- Make the imagery visually distinctive and cinematic.
- Visual style: stylized 3D animated family-film look, expressive faces, rounded shapes, soft magical lighting, painterly textures, whimsical storybook atmosphere.
- Avoid photorealistic live-action actors, documentary realism, uncanny faces, harsh realism, horror, or adult drama aesthetics.
- Include a continuity report and token budget estimate.
- Prioritize stable character identity: age, face, hair, clothing, silhouette, props, and emotional state must remain coherent across all shots.
- If the user includes explicit character locking requirements in the premise, obey them strictly and reflect them consistently in the Character Continuity Bible.
"""


def _make_schema_strict(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Adapt a Pydantic JSON schema for OpenAI Structured Outputs.

    OpenAI expects every object in a strict schema to declare
    additionalProperties: false. We also make required fields explicit.
    """

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object":
                node["additionalProperties"] = False
                properties = node.get("properties")
                if isinstance(properties, dict):
                    node["required"] = list(properties.keys())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(schema)
    return schema


def _story_package_json_schema() -> Dict[str, Any]:
    schema = StoryPackage.model_json_schema()
    return _make_schema_strict(schema)


class OpenAIStoryClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self._client = None
        if self.api_key:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ImportError(
                    "The openai package is required for live generation. Install dependencies with: "
                    "python -m pip install -r requirements.txt"
                ) from exc
            self._client = OpenAI(api_key=self.api_key)

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key)

    def generate_story_package(self, premise: str, use_mock: bool = False) -> StoryPackage:
        if use_mock or not self._client:
            return get_sample_story_package()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(premise=premise)},
        ]

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "story_package",
                    "schema": _story_package_json_schema(),
                    "strict": True,
                },
            },
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenAI returned an empty response.")
        data = json.loads(content)
        return StoryPackage.model_validate(data)
