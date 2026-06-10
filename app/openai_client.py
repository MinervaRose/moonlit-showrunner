from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from app.schemas import StoryPackage
from app.sample_data import get_sample_story_package

load_dotenv()

SYSTEM_PROMPT = """You are Moonlit Showrunner, an AI creative production pipeline.
You transform a short premise into a coherent, emotionally satisfying short-drama production package.
You must optimize for clear visual storytelling, low dialogue, strong emotional arc, and practical MP4 assembly.
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
- Each video prompt must be usable for image or video generation.
- Include a continuity report and token budget estimate.
"""


def _make_schema_strict(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Adapt a Pydantic JSON schema for OpenAI Structured Outputs.

    OpenAI requires every object in a strict JSON schema to declare:
    - additionalProperties: false
    - required: [all defined properties]
    """

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object":
                node["additionalProperties"] = False
                if "properties" in node and isinstance(node["properties"], dict):
                    node["required"] = list(node["properties"].keys())

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
