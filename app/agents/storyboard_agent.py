from __future__ import annotations

from app.schemas import StoryPackage


class StoryboardAgent:
    """Lightweight semantic wrapper for the Moonlit Showrunner pipeline.

    Version 1 uses one schema-driven LLM call for reliability and token efficiency.
    These agent classes make the architecture explicit and provide extension points
    for future multi-call or multi-provider workflows.
    """

    name = "StoryboardAgent"

    def summarize(self, package: StoryPackage) -> str:
        return f"{self.name} processed '{package.brief.title}'."
