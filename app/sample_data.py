from __future__ import annotations

from app.schemas import StoryPackage

SAMPLE_PREMISE = (
    "A small kitten places his first lost tooth on a tiny moonlit cushion beside his bed basket, "
    "worried that growing up means losing a little piece of himself. At midnight, the tooth opens "
    "a glowing silver doorway into a hidden fairy archive where cherished keepsakes become stars. "
    "By morning, he finds a coin and a faint sparkle on the windowsill, while the viewer sees the "
    "tooth fairy slipping into the dawn."
)

SAMPLE_STORY_PACKAGE = {
    "brief": {
        "title": "The Little Tooth Door",
        "logline": "A thoughtful kitten discovers that growing up does not erase wonder; it turns tiny losses into stars.",
        "genre": "magical family micro-drama",
        "target_duration_seconds": 48,
        "emotional_theme": "Growing up can feel like losing something, but memory can transform loss into wonder.",
        "tone": "tender, moonlit, whimsical, quietly emotional",
        "audience": "general audience, family-friendly short-form viewers"
    },
    "characters": [
        {
            "name": "Milo",
            "role": "protagonist",
            "description": "A thoughtful little kitten who has just lost his first tooth.",
            "emotional_arc": "He begins worried that growing up means losing a piece of himself, and ends reassured by a magical sign.",
            "visual_notes": "Soft brown-and-cream fur, hazel eyes, tiny paws, and a little white tooth held carefully in his paw."
        },
        {
            "name": "The Tooth Fairy",
            "role": "magical guide",
            "description": "A tiny moonlit figure who silently archives cherished keepsakes as stars.",
            "emotional_arc": "She remains mysterious, but her gentle work reframes Milo’s fear.",
            "visual_notes": "Dainty silhouette with delicate wings, blue eyes, short white hair, blue gown embroidered with tiny teeth, never fully revealed until dawn."
        }
    ],
    "scenes": [
        {
            "scene_number": 1,
            "title": "The First Tooth",
            "duration_seconds": 7,
            "location": "Milo’s cozy sleeping nook at bedtime",
            "action": "Milo studies the tiny tooth in his paw, unsure whether to be proud or sad.",
            "emotional_beat": "A small milestone feels strangely enormous.",
            "dialogue_or_caption": "What if growing up means pieces of me disappear?",
            "camera_direction": "Close-up on the tooth, then tilt up to Milo’s thoughtful face.",
            "sound_or_music_notes": "Soft music box notes, distant night ambience."
        },
        {
            "scene_number": 2,
            "title": "Under the Pillow",
            "duration_seconds": 6,
            "location": "Beside a bed basket, blue moonlight",
            "action": "Milo places the tooth on a tiny moonlit cushion beside his basket and slowly falls asleep.",
            "emotional_beat": "Trusting the unknown.",
            "dialogue_or_caption": "He lets the night keep it safe.",
            "camera_direction": "Gentle overhead shot as his paw withdraws from beside the moonlit cushion.",
            "sound_or_music_notes": "Music lowers to a hush."
        },
        {
            "scene_number": 3,
            "title": "The Moonlit Door",
            "duration_seconds": 8,
            "location": "Beside the moonlit cushion, transformed into a tiny glowing threshold",
            "action": "The tooth begins to glow, opening a small door made of silver dust.",
            "emotional_beat": "Ordinary kittenhood becomes secret magic.",
            "dialogue_or_caption": "At midnight, the smallest things know the way.",
            "camera_direction": "Macro shot moving toward the glowing door.",
            "sound_or_music_notes": "Tiny bells, soft whoosh of moonlight."
        },
        {
            "scene_number": 4,
            "title": "The Archive of Stars",
            "duration_seconds": 10,
            "location": "A hidden fairy archive in the sky",
            "action": "Fairies carry the tooth through shelves of glowing keepsakes and place it among newborn stars.",
            "emotional_beat": "Loss becomes preservation.",
            "dialogue_or_caption": "Nothing loved is lost. It learns to shine differently.",
            "camera_direction": "Wide shot of floating shelves and star jars, slow cinematic drift.",
            "sound_or_music_notes": "Warm orchestral swell, airy chimes."
        },
        {
            "scene_number": 5,
            "title": "Morning Coin",
            "duration_seconds": 7,
            "location": "Milo’s cozy nook at sunrise",
            "action": "Milo wakes, finds a coin beside the cushion, and notices a sparkle on the windowsill.",
            "emotional_beat": "Reassurance arrives gently.",
            "dialogue_or_caption": "In the morning, something new was waiting.",
            "camera_direction": "Warm sunrise close-up on his delighted expression and the tiny sparkle.",
            "sound_or_music_notes": "Music resolves softly."
        },
        {
            "scene_number": 6,
            "title": "The Last Glimpse",
            "duration_seconds": 6,
            "location": "Outside the open window at dawn",
            "action": "The viewer sees the tooth fairy slip into the golden sky before Milo looks back.",
            "emotional_beat": "Magic remains half-seen, but fully felt.",
            "dialogue_or_caption": "Some doors only open while we are dreaming.",
            "camera_direction": "Silhouette shot, then fade to white-gold dawn.",
            "sound_or_music_notes": "Final bell tone, birdsong."
        }
    ],
    "storyboard": [
        {"shot_number": 1, "scene_number": 1, "shot_type": "close-up", "visual_description": "Tiny tooth in a kitten's paw under warm bedside light.", "camera_movement": "slow tilt", "lighting": "warm lamp and blue moon edge light", "transition": "fade in"},
        {"shot_number": 2, "scene_number": 2, "shot_type": "overhead", "visual_description": "Small paw placing the tooth onto a tiny moonlit cushion.", "camera_movement": "still, gentle", "lighting": "soft blue moonlight", "transition": "dissolve"},
        {"shot_number": 3, "scene_number": 3, "shot_type": "macro fantasy", "visual_description": "The tooth glowing and opening a tiny silver door.", "camera_movement": "push in", "lighting": "silver glow", "transition": "sparkle wipe"},
        {"shot_number": 4, "scene_number": 4, "shot_type": "wide fantasy", "visual_description": "Fairy archive filled with glowing memory stars.", "camera_movement": "slow drift", "lighting": "moonlit, pearly, celestial", "transition": "match cut"},
        {"shot_number": 5, "scene_number": 5, "shot_type": "medium close-up", "visual_description": "Milo looking happily at a coin and a sparkle on the windowsill.", "camera_movement": "gentle reveal", "lighting": "gold sunrise", "transition": "warm dissolve"},
        {"shot_number": 6, "scene_number": 6, "shot_type": "silhouette", "visual_description": "Tiny fairy slipping out through the dawn window as the kitten watches the sparkle linger.", "camera_movement": "slow pull back", "lighting": "golden dawn", "transition": "fade out"}
    ],
    "visual_style_bible": {
        "overall_style": "storybook cinematic fantasy with soft magical details",
        "color_palette": "moonlit blues, pearl silver, warm gold, soft lavender",
        "lighting_rules": "Night scenes use blue moonlight and silver glow; morning scenes use warm gold.",
        "character_consistency_rules": "Milo always has soft brown-and-cream fur, hazel eyes, a gentle expressive kitten face, and an optional pale blue moon-pattern neckerchief; the tooth fairy remains dainty with blue eyes, short white hair, and a blue gown embroidered with tiny teeth.",
        "world_design_notes": "The fairy archive should feel like a tiny library in the sky, with glowing jars and star shelves."
    },
    "character_continuity_profiles": [
        {
            "name": "Milo",
            "stable_identity": "A thoughtful small kitten named Milo; the same kitten must appear in every cozy-room shot.",
            "face_and_body": "Round soft kitten face, small kitten proportions, expressive posture, gentle and curious presence.",
            "hair_and_eyes": "Hazel eyes and warm brown fur with soft loose curls around the forehead and cheeks, consistent silhouette.",
            "clothing_and_props": "Soft brown-and-cream fur, optional pale blue moon-pattern neckerchief, tiny white baby tooth appears in early shots; coin appears only in the morning shot.",
            "expression_and_movement": "Quiet, tender, slightly worried at night; relieved, curious, and softly delighted by morning.",
            "do_not_change": [
                "Do not change Milo's fur pattern, hazel eyes, curled forehead fur, or facial proportions between shots.",
                "Do not make Milo look like a different kitten in later clips.",
                "Do not switch to photorealistic animal rendering or realistic live-action footage."
            ]
        },
        {
            "name": "The Tooth Fairy",
            "stable_identity": "A tiny moonlit fairy archivist who remains delicate, luminous, and mysterious.",
            "face_and_body": "Very small graceful silhouette, dainty design, delicate wings, no uncanny realism.",
            "hair_and_eyes": "Blue eyes, short white hair, and a delicate face remain visible when seen closely; overall design stays soft and magical.",
            "clothing_and_props": "Blue gown embroidered with tiny teeth, transparent wings, faint star-dust trail, carries the glowing tooth in archive shots.",
            "expression_and_movement": "Silent, gentle, careful, floating or gliding rather than dramatic flying.",
            "do_not_change": [
                "Do not make the fairy frightening, adult-glamorous, monstrous, or photorealistic.",
                "Keep the fairy small, luminous, and delicate across shots.",
                "Use the same blue gown, short white hair, blue eyes, and delicate wing silhouette whenever she appears."
            ]
        }
    ],
    "global_continuity_lock": {
        "visual_style_lock": "Stylized 3D animated family-film look with soft storybook textures, rounded forms, expressive but non-photorealistic characters.",
        "character_locking_rules": "Reuse the character continuity profiles in every image and video prompt. Preserve age, hairstyle, clothing, silhouette, and signature props unless the story explicitly changes them.",
        "palette_and_lighting_lock": "Night scenes stay in moonlit blue, pearl silver, and soft lavender; morning scenes move to warm gold while preserving the same character designs.",
        "environment_rules": "Milo's cozy room keeps the same sleeping basket, moonlit cushion, window, and moonlit atmosphere. The fairy archive remains celestial, tiny, and library-like.",
        "negative_continuity_rules": "No realistic actors, no character age changes, no clothing swaps, no changing ethnicity or facial structure, no horror tone, no logos, no readable text."
    },
    "shot_continuity_notes": [
        {
            "shot_number": 1,
            "characters_present": ["Milo"],
            "continuity_from_previous_shot": "Opening shot establishes Milo's stable design.",
            "required_character_details": "Milo is a small brown-and-cream kitten with hazel eyes, soft loose curls in his forehead fur, and an optional pale blue moon-pattern neckerchief.",
            "props_and_costume_state": "Tiny white tooth in his paw; fur pattern and optional neckerchief unchanged.",
            "environment_state": "Cozy room, warm bedside lamp plus blue moon edge light.",
            "consistency_risk": "Hands or face could be distorted; keep kitten-friendly stylized proportions.",
            "prompt_anchor": "Milo must be the same round-faced kitten with hazel eyes and warm brown-and-cream fur throughout all cozy-room shots."
        },
        {
            "shot_number": 2,
            "characters_present": ["Milo"],
            "continuity_from_previous_shot": "Milo remains the same kitten from shot 1, now placing the same tooth onto the moonlit cushion beside his basket.",
            "required_character_details": "Same hazel eyes, same curled forehead fur, same small kitten proportions, same optional pale blue moon-pattern neckerchief.",
            "props_and_costume_state": "Tooth moves from his paw to the moonlit cushion beside the basket.",
            "environment_state": "Same cozy room, sleeping basket, moonlit cushion, and moonlit palette.",
            "consistency_risk": "Overhead angle may hide face; retain identifiable fur pattern, curled forehead fur, hazel eyes when visible, and paw scale.",
            "prompt_anchor": "Preserve Milo's kitten silhouette, warm brown-and-cream fur, and optional pale blue moon-pattern neckerchief from shot 1."
        },
        {
            "shot_number": 3,
            "characters_present": [],
            "continuity_from_previous_shot": "The same tooth placed on the moonlit cushion becomes the glowing doorway.",
            "required_character_details": "No full character visible; focus on the same tooth and moonlit cushion environment.",
            "props_and_costume_state": "Tooth glows on the same moonlit cushion.",
            "environment_state": "Macro view beside Milo's moonlit cushion, moonlit blue and silver glow.",
            "consistency_risk": "Doorway could feel disconnected; keep cushion fabric and tooth shape consistent.",
            "prompt_anchor": "The glowing tooth is the same tooth from Milo's paw, now on the same moonlit cushion."
        },
        {
            "shot_number": 4,
            "characters_present": ["The Tooth Fairy"],
            "continuity_from_previous_shot": "The glowing doorway leads to the fairy archive; the tooth remains the central prop.",
            "required_character_details": "Tooth fairy is tiny, luminous, silver-gold, delicate, and non-scary.",
            "props_and_costume_state": "The fairy carries or guides the glowing tooth through star shelves.",
            "environment_state": "Celestial archive with glowing memory jars and star shelves.",
            "consistency_risk": "Fairy could become too detailed or glamorous; keep her small, simple, luminous.",
            "prompt_anchor": "The fairy is always a tiny moonlit archivist with delicate wings and silver-gold glow."
        },
        {
            "shot_number": 5,
            "characters_present": ["Milo"],
            "continuity_from_previous_shot": "Return to the same cozy room in morning; Milo is the same kitten from shots 1 and 2.",
            "required_character_details": "Same warm brown-and-cream fur, same curled forehead fur, same hazel eyes, same round kitten face, same optional pale blue moon-pattern neckerchief.",
            "props_and_costume_state": "Tooth is gone; coin and faint sparkle are now present.",
            "environment_state": "Same sleeping basket, moonlit cushion, and window, now lit by warm sunrise.",
            "consistency_risk": "Milo's face may drift after the archive shot; strongly preserve the established design.",
            "prompt_anchor": "Milo must match the kitten from shots 1 and 2, only her emotion changes to relief."
        },
        {
            "shot_number": 6,
            "characters_present": ["The Tooth Fairy"],
            "continuity_from_previous_shot": "The fairy leaves the same cozy-room window after completing the exchange.",
            "required_character_details": "Same tiny silver-gold fairy silhouette with delicate wings.",
            "props_and_costume_state": "No tooth visible; faint sparkle trail remains.",
            "environment_state": "Outside Milo's same window at golden dawn.",
            "consistency_risk": "Fairy could look like a different creature; preserve tiny archivist silhouette.",
            "prompt_anchor": "The fairy keeps the same tiny luminous winged silhouette from the archive shot."
        }
    ],
    "video_prompts": [
        {"shot_number": 1, "prompt": "Cinematic storybook close-up of a tiny baby tooth resting in a little kitten's palm, warm bedside lamp, blue moon edge light, tender magical mood", "negative_prompt": "scary, horror, distorted hands, extra fingers", "duration_seconds": 7},
        {"shot_number": 2, "prompt": "Overhead shot of a kitten placing a tiny tooth onto a moonlit cushion in a cozy magical room, gentle emotional atmosphere", "negative_prompt": "dark horror, messy room, harsh lighting", "duration_seconds": 6},
        {"shot_number": 3, "prompt": "Macro fantasy shot of a tiny tooth glowing on a moonlit cushion and opening a miniature silver moonlit doorway, sparkling dust, magical realism", "negative_prompt": "creepy, insects, grotesque", "duration_seconds": 8},
        {"shot_number": 4, "prompt": "Wide cinematic shot of a hidden fairy archive in the sky, tiny fairies carrying a glowing tooth, shelves of memory stars, pearl and moonlight palette", "negative_prompt": "crowded chaos, dark villain, horror", "duration_seconds": 10},
        {"shot_number": 5, "prompt": "Warm sunrise cozy room scene, little kitten discovering a coin beside the moonlit cushion and a faint sparkle on the windowsill, gentle delighted expression", "negative_prompt": "sad ending, harsh shadows", "duration_seconds": 7},
        {"shot_number": 6, "prompt": "Tiny tooth fairy silhouette slipping out of a window into golden dawn, delicate wings, magical final glimpse, cinematic fade", "negative_prompt": "monster, scary fairy, dark mood", "duration_seconds": 6}
    ],
    "continuity_report": {
        "strengths": ["The emotional arc is simple and readable.", "The visual transition from blue night to golden morning supports the theme.", "The fairy is mysterious without distracting from Milo."],
        "risks": ["The fairy archive could feel too abstract if not visually anchored.", "Milo's worry must remain gentle, not frightening."],
        "fixes_applied": ["Kept dialogue minimal and caption-driven.", "Used repeated visual symbols: tooth, moonlight, sparkle, window.", "Limited the story to six scenes for clarity."],
        "final_assessment": "The story is coherent, emotionally complete, and suitable for a short magical kitten-centered MP4."
    },
    "edit_decisions": [
        {"order": 1, "scene_number": 1, "shot_number": 1, "duration_seconds": 7, "on_screen_text": "What if growing up means pieces of me disappear?", "transition": "fade in", "audio_note": "music box begins"},
        {"order": 2, "scene_number": 2, "shot_number": 2, "duration_seconds": 6, "on_screen_text": "He lets the night keep it safe.", "transition": "soft dissolve", "audio_note": "music lowers"},
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
