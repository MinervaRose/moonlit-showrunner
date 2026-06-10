from __future__ import annotations

from app.schemas import StoryPackage

SAMPLE_PREMISE = (
    "A little girl places her first lost tooth under her pillow, afraid that growing up "
    "means losing pieces of herself. At midnight, the tooth opens a tiny moonlit doorway "
    "into a hidden fairy archive where children’s memories become stars. By morning, she "
    "finds a coin and a faint sparkle on the windowsill, while the viewer sees the tooth "
    "fairy slipping into the dawn."
)

SAMPLE_STORY_PACKAGE = {
    "brief": {
        "title": "The Little Tooth Door",
        "logline": "A nervous child discovers that growing up does not erase childhood; it turns memories into stars.",
        "genre": "magical family micro-drama",
        "target_duration_seconds": 48,
        "emotional_theme": "Growing up can feel like losing something, but memory can transform loss into wonder.",
        "tone": "tender, moonlit, whimsical, quietly emotional",
        "audience": "general audience, family-friendly short-form viewers"
    },
    "characters": [
        {
            "name": "Mina",
            "role": "protagonist",
            "description": "A thoughtful little girl who has just lost her first tooth.",
            "emotional_arc": "She begins worried that growing up means losing herself, and ends reassured by a magical sign.",
            "visual_notes": "Soft pajamas, expressive eyes, small hand holding a tiny tooth."
        },
        {
            "name": "The Tooth Fairy",
            "role": "magical guide",
            "description": "A tiny moonlit figure who silently archives children’s memories as stars.",
            "emotional_arc": "She remains mysterious, but her gentle work reframes Mina’s fear.",
            "visual_notes": "Silhouette with delicate wings, silver glow, never fully revealed until dawn."
        }
    ],
    "scenes": [
        {
            "scene_number": 1,
            "title": "The First Tooth",
            "duration_seconds": 7,
            "location": "Mina’s bedroom at bedtime",
            "action": "Mina studies the tiny tooth in her palm, unsure whether to be proud or sad.",
            "emotional_beat": "A small milestone feels strangely enormous.",
            "dialogue_or_caption": "What if growing up means pieces of me disappear?",
            "camera_direction": "Close-up on the tooth, then tilt up to Mina’s worried face.",
            "sound_or_music_notes": "Soft music box notes, distant night ambience."
        },
        {
            "scene_number": 2,
            "title": "Under the Pillow",
            "duration_seconds": 6,
            "location": "Bedside, blue moonlight",
            "action": "Mina slides the tooth under her pillow and slowly falls asleep.",
            "emotional_beat": "Trusting the unknown.",
            "dialogue_or_caption": "She lets the night keep it safe.",
            "camera_direction": "Gentle overhead shot as her hand withdraws from beneath the pillow.",
            "sound_or_music_notes": "Music lowers to a hush."
        },
        {
            "scene_number": 3,
            "title": "The Moonlit Door",
            "duration_seconds": 8,
            "location": "Beneath the pillow, transformed into a tiny glowing threshold",
            "action": "The tooth begins to glow, opening a small door made of silver dust.",
            "emotional_beat": "Ordinary childhood becomes secret magic.",
            "dialogue_or_caption": "At midnight, the smallest things know the way.",
            "camera_direction": "Macro shot moving toward the glowing door.",
            "sound_or_music_notes": "Tiny bells, soft whoosh of moonlight."
        },
        {
            "scene_number": 4,
            "title": "The Archive of Stars",
            "duration_seconds": 10,
            "location": "A hidden fairy archive in the sky",
            "action": "Fairies carry the tooth through shelves of glowing memories and place it among newborn stars.",
            "emotional_beat": "Loss becomes preservation.",
            "dialogue_or_caption": "Nothing loved is lost. It learns to shine differently.",
            "camera_direction": "Wide shot of floating shelves and star jars, slow cinematic drift.",
            "sound_or_music_notes": "Warm orchestral swell, airy chimes."
        },
        {
            "scene_number": 5,
            "title": "Morning Coin",
            "duration_seconds": 7,
            "location": "Mina’s bedroom at sunrise",
            "action": "Mina wakes, finds a coin under the pillow, and notices a sparkle on the windowsill.",
            "emotional_beat": "Reassurance arrives gently.",
            "dialogue_or_caption": "In the morning, something new was waiting.",
            "camera_direction": "Warm sunrise close-up on her smile and the tiny sparkle.",
            "sound_or_music_notes": "Music resolves softly."
        },
        {
            "scene_number": 6,
            "title": "The Last Glimpse",
            "duration_seconds": 6,
            "location": "Outside the open window at dawn",
            "action": "The viewer sees the tooth fairy slip into the golden sky before Mina looks back.",
            "emotional_beat": "Magic remains half-seen, but fully felt.",
            "dialogue_or_caption": "Some doors only open while we are dreaming.",
            "camera_direction": "Silhouette shot, then fade to white-gold dawn.",
            "sound_or_music_notes": "Final bell tone, birdsong."
        }
    ],
    "storyboard": [
        {"shot_number": 1, "scene_number": 1, "shot_type": "close-up", "visual_description": "Tiny tooth in a child's palm under warm bedside light.", "camera_movement": "slow tilt", "lighting": "warm lamp and blue moon edge light", "transition": "fade in"},
        {"shot_number": 2, "scene_number": 2, "shot_type": "overhead", "visual_description": "Small hand placing the tooth beneath a pillow.", "camera_movement": "still, gentle", "lighting": "soft blue moonlight", "transition": "dissolve"},
        {"shot_number": 3, "scene_number": 3, "shot_type": "macro fantasy", "visual_description": "The tooth glowing and opening a tiny silver door.", "camera_movement": "push in", "lighting": "silver glow", "transition": "sparkle wipe"},
        {"shot_number": 4, "scene_number": 4, "shot_type": "wide fantasy", "visual_description": "Fairy archive filled with glowing memory stars.", "camera_movement": "slow drift", "lighting": "moonlit, pearly, celestial", "transition": "match cut"},
        {"shot_number": 5, "scene_number": 5, "shot_type": "medium close-up", "visual_description": "Mina smiling at a coin and a sparkle on the windowsill.", "camera_movement": "gentle reveal", "lighting": "gold sunrise", "transition": "warm dissolve"},
        {"shot_number": 6, "scene_number": 6, "shot_type": "silhouette", "visual_description": "Tiny fairy slipping out through the dawn window.", "camera_movement": "slow pull back", "lighting": "golden dawn", "transition": "fade out"}
    ],
    "visual_style_bible": {
        "overall_style": "storybook cinematic realism with soft magical details",
        "color_palette": "moonlit blues, pearl silver, warm gold, soft lavender",
        "lighting_rules": "Night scenes use blue moonlight and silver glow; morning scenes use warm gold.",
        "character_consistency_rules": "Mina always has soft pajamas and expressive eyes; the tooth fairy remains mostly silhouetted with silver wings.",
        "world_design_notes": "The fairy archive should feel like a tiny library in the sky, with glowing jars and star shelves."
    },
    "video_prompts": [
        {"shot_number": 1, "prompt": "Cinematic storybook close-up of a tiny baby tooth resting in a little girl's palm, warm bedside lamp, blue moon edge light, tender magical mood", "negative_prompt": "scary, horror, distorted hands, extra fingers", "duration_seconds": 7},
        {"shot_number": 2, "prompt": "Overhead shot of a child placing a tiny tooth under a pillow in a moonlit bedroom, soft pajamas, gentle emotional atmosphere", "negative_prompt": "dark horror, messy room, harsh lighting", "duration_seconds": 6},
        {"shot_number": 3, "prompt": "Macro fantasy shot of a tiny tooth glowing under a pillow and opening a miniature silver moonlit doorway, sparkling dust, magical realism", "negative_prompt": "creepy, insects, grotesque", "duration_seconds": 8},
        {"shot_number": 4, "prompt": "Wide cinematic shot of a hidden fairy archive in the sky, tiny fairies carrying a glowing tooth, shelves of memory stars, pearl and moonlight palette", "negative_prompt": "crowded chaos, dark villain, horror", "duration_seconds": 10},
        {"shot_number": 5, "prompt": "Warm sunrise bedroom scene, little girl discovering a coin under her pillow and a faint sparkle on the windowsill, gentle smile", "negative_prompt": "sad ending, harsh shadows", "duration_seconds": 7},
        {"shot_number": 6, "prompt": "Tiny tooth fairy silhouette slipping out of a window into golden dawn, delicate wings, magical final glimpse, cinematic fade", "negative_prompt": "monster, scary fairy, dark mood", "duration_seconds": 6}
    ],
    "continuity_report": {
        "strengths": ["The emotional arc is simple and readable.", "The visual transition from blue night to golden morning supports the theme.", "The fairy is mysterious without distracting from Mina."],
        "risks": ["The fairy archive could feel too abstract if not visually anchored.", "Mina's fear must remain gentle, not frightening."],
        "fixes_applied": ["Kept dialogue minimal and caption-driven.", "Used repeated visual symbols: tooth, moonlight, sparkle, window.", "Limited the story to six scenes for clarity."],
        "final_assessment": "The story is coherent, emotionally complete, and suitable for a short magical MP4."
    },
    "edit_decisions": [
        {"order": 1, "scene_number": 1, "shot_number": 1, "duration_seconds": 7, "on_screen_text": "What if growing up means pieces of me disappear?", "transition": "fade in", "audio_note": "music box begins"},
        {"order": 2, "scene_number": 2, "shot_number": 2, "duration_seconds": 6, "on_screen_text": "She lets the night keep it safe.", "transition": "soft dissolve", "audio_note": "music lowers"},
        {"order": 3, "scene_number": 3, "shot_number": 3, "duration_seconds": 8, "on_screen_text": "At midnight, the smallest things know the way.", "transition": "sparkle wipe", "audio_note": "bells shimmer"},
        {"order": 4, "scene_number": 4, "shot_number": 4, "duration_seconds": 10, "on_screen_text": "Nothing loved is lost. It learns to shine differently.", "transition": "match cut", "audio_note": "orchestral swell"},
        {"order": 5, "scene_number": 5, "shot_number": 5, "duration_seconds": 7, "on_screen_text": "In the morning, something new was waiting.", "transition": "warm dissolve", "audio_note": "gentle resolution"},
        {"order": 6, "scene_number": 6, "shot_number": 6, "duration_seconds": 6, "on_screen_text": "Some doors only open while we are dreaming.", "transition": "fade out", "audio_note": "birdsong and final bell"}
    ],
    "token_budget": {
        "estimated_prompt_tokens": 1200,
        "estimated_completion_tokens": 2500,
        "token_saving_strategy": "Use one compact schema-driven generation call, then validate and reuse structured scene fields instead of repeatedly resending the full story."
    }
}

def get_sample_story_package() -> StoryPackage:
    return StoryPackage.model_validate(SAMPLE_STORY_PACKAGE)
