from __future__ import annotations

from app.schemas import StoryPackage


def _truncate(text: str, max_chars: int = 900) -> str:
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[: max_chars - 3] + "..."


def build_character_bible_block(package: StoryPackage) -> str:
    """Return a compact continuity bible suitable for image/video prompts."""
    parts: list[str] = ["CHARACTER CONTINUITY BIBLE — preserve these details across every shot:"]
    for profile in package.character_continuity_profiles:
        rules = "; ".join(profile.do_not_change)
        parts.append(
            f"{profile.name}: {profile.stable_identity} "
            f"Face/body: {profile.face_and_body}. Hair/eyes: {profile.hair_and_eyes}. "
            f"Clothing/props: {profile.clothing_and_props}. Movement/expression: {profile.expression_and_movement}. "
            f"Do not change: {rules}."
        )
    return _truncate("\n".join(parts), 1600)


def build_global_continuity_block(package: StoryPackage) -> str:
    lock = package.global_continuity_lock
    return _truncate(
        "GLOBAL CONTINUITY LOCK — "
        f"Visual style: {lock.visual_style_lock}. "
        f"Character rules: {lock.character_locking_rules}. "
        f"Palette/lighting: {lock.palette_and_lighting_lock}. "
        f"Environment: {lock.environment_rules}. "
        f"Avoid: {lock.negative_continuity_rules}.",
        1200,
    )


def build_shot_continuity_block(package: StoryPackage, shot_number: int) -> str:
    note = next((n for n in package.shot_continuity_notes if n.shot_number == shot_number), None)
    if not note:
        return "SHOT CONTINUITY: preserve the same recurring characters, clothing, props, palette, and environment established in the story package."
    return _truncate(
        "SHOT CONTINUITY MEMORY — "
        f"Characters present: {', '.join(note.characters_present) or 'none visible'}. "
        f"From previous shot: {note.continuity_from_previous_shot}. "
        f"Required character details: {note.required_character_details}. "
        f"Props/costume: {note.props_and_costume_state}. "
        f"Environment: {note.environment_state}. "
        f"Risk to avoid: {note.consistency_risk}. "
        f"Anchor: {note.prompt_anchor}.",
        1100,
    )


def build_full_continuity_prompt_block(package: StoryPackage, shot_number: int) -> str:
    return "\n".join(
        [
            build_global_continuity_block(package),
            build_character_bible_block(package),
            build_shot_continuity_block(package, shot_number),
        ]
    )
