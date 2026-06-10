from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class Character(BaseModel):
    name: str
    role: str
    description: str
    emotional_arc: str
    visual_notes: str


class StoryBrief(BaseModel):
    title: str
    logline: str
    genre: str
    target_duration_seconds: int = Field(ge=20, le=120)
    emotional_theme: str
    tone: str
    audience: str


class Scene(BaseModel):
    scene_number: int
    title: str
    duration_seconds: int = Field(ge=3, le=30)
    location: str
    action: str
    emotional_beat: str
    dialogue_or_caption: str
    camera_direction: str
    sound_or_music_notes: str


class StoryboardShot(BaseModel):
    shot_number: int
    scene_number: int
    shot_type: str
    visual_description: str
    camera_movement: str
    lighting: str
    transition: str


class VisualStyleBible(BaseModel):
    overall_style: str
    color_palette: str
    lighting_rules: str
    character_consistency_rules: str
    world_design_notes: str


class VideoPrompt(BaseModel):
    shot_number: int
    prompt: str
    negative_prompt: Optional[str] = ""
    duration_seconds: int = Field(ge=3, le=20)


class ContinuityReport(BaseModel):
    strengths: List[str]
    risks: List[str]
    fixes_applied: List[str]
    final_assessment: str


class EditDecision(BaseModel):
    order: int
    scene_number: int
    shot_number: int
    duration_seconds: int = Field(ge=3, le=20)
    on_screen_text: str
    transition: str
    audio_note: str


class TokenBudget(BaseModel):
    estimated_prompt_tokens: int
    estimated_completion_tokens: int
    token_saving_strategy: str


class StoryPackage(BaseModel):
    brief: StoryBrief
    characters: List[Character]
    scenes: List[Scene]
    storyboard: List[StoryboardShot]
    visual_style_bible: VisualStyleBible
    video_prompts: List[VideoPrompt]
    continuity_report: ContinuityReport
    edit_decisions: List[EditDecision]
    token_budget: TokenBudget

    def to_markdown(self) -> str:
        lines = []
        lines.append(f"# {self.brief.title}\n")
        lines.append(f"**Logline:** {self.brief.logline}\n")
        lines.append(f"**Genre:** {self.brief.genre}\n")
        lines.append(f"**Tone:** {self.brief.tone}\n")
        lines.append(f"**Theme:** {self.brief.emotional_theme}\n")

        lines.append("\n## Characters\n")
        for c in self.characters:
            lines.append(f"### {c.name}")
            lines.append(f"- **Role:** {c.role}")
            lines.append(f"- **Description:** {c.description}")
            lines.append(f"- **Arc:** {c.emotional_arc}")
            lines.append(f"- **Visual notes:** {c.visual_notes}\n")

        lines.append("\n## Scenes\n")
        for s in self.scenes:
            lines.append(f"### Scene {s.scene_number}: {s.title}")
            lines.append(f"- **Duration:** {s.duration_seconds}s")
            lines.append(f"- **Location:** {s.location}")
            lines.append(f"- **Action:** {s.action}")
            lines.append(f"- **Emotional beat:** {s.emotional_beat}")
            lines.append(f"- **Caption/dialogue:** {s.dialogue_or_caption}")
            lines.append(f"- **Camera:** {s.camera_direction}")
            lines.append(f"- **Sound:** {s.sound_or_music_notes}\n")

        lines.append("\n## Storyboard\n")
        for shot in self.storyboard:
            lines.append(f"### Shot {shot.shot_number} / Scene {shot.scene_number}")
            lines.append(f"- **Type:** {shot.shot_type}")
            lines.append(f"- **Visual:** {shot.visual_description}")
            lines.append(f"- **Movement:** {shot.camera_movement}")
            lines.append(f"- **Lighting:** {shot.lighting}")
            lines.append(f"- **Transition:** {shot.transition}\n")

        lines.append("\n## Visual Style Bible\n")
        lines.append(f"- **Style:** {self.visual_style_bible.overall_style}")
        lines.append(f"- **Palette:** {self.visual_style_bible.color_palette}")
        lines.append(f"- **Lighting:** {self.visual_style_bible.lighting_rules}")
        lines.append(f"- **Character consistency:** {self.visual_style_bible.character_consistency_rules}")
        lines.append(f"- **World design:** {self.visual_style_bible.world_design_notes}\n")

        lines.append("\n## Video Prompts\n")
        for vp in self.video_prompts:
            lines.append(f"### Shot {vp.shot_number}")
            lines.append(vp.prompt)
            if vp.negative_prompt:
                lines.append(f"\n**Negative prompt:** {vp.negative_prompt}")
            lines.append("")

        lines.append("\n## Continuity Report\n")
        lines.append("**Strengths:**")
        for item in self.continuity_report.strengths:
            lines.append(f"- {item}")
        lines.append("\n**Risks:**")
        for item in self.continuity_report.risks:
            lines.append(f"- {item}")
        lines.append("\n**Fixes applied:**")
        for item in self.continuity_report.fixes_applied:
            lines.append(f"- {item}")
        lines.append(f"\n**Final assessment:** {self.continuity_report.final_assessment}\n")

        lines.append("\n## Edit Decision List\n")
        for e in self.edit_decisions:
            lines.append(
                f"{e.order}. Scene {e.scene_number}, Shot {e.shot_number} — {e.duration_seconds}s — "
                f"{e.transition} — {e.on_screen_text}"
            )

        lines.append("\n## Token Budget\n")
        lines.append(f"- Estimated prompt tokens: {self.token_budget.estimated_prompt_tokens}")
        lines.append(f"- Estimated completion tokens: {self.token_budget.estimated_completion_tokens}")
        lines.append(f"- Strategy: {self.token_budget.token_saving_strategy}")

        return "\n".join(lines)
