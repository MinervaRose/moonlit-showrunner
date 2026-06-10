from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.pipeline import MoonlitPipeline
from app.sample_data import SAMPLE_PREMISE

st.set_page_config(
    page_title="Moonlit Showrunner",
    page_icon="🌙",
    layout="wide",
)

st.title("Moonlit Showrunner")
st.caption("An AI-assisted short-drama pipeline with character locking, continuity-aware image generation, visual animatics, and optional full Sora video generation")

st.info(
    "**Version note:** v0.7.2 keeps character locking and moderation-aware Sora prompt sanitization, and pivots the default story to a safer kitten protagonist. The app can generate reusable character reference cards first, then use those reference cards to guide scene image generation. Continuity prompts still support the Sora workflow, while the visual animatic remains the fast default."
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenAI text model", value=st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini"))
    image_model = st.text_input("OpenAI image model", value=st.secrets.get("OPENAI_IMAGE_MODEL", "gpt-image-1"))
    video_model = st.text_input("OpenAI video model", value=st.secrets.get("OPENAI_VIDEO_MODEL", "sora-2"))
    sora_enabled = st.checkbox(
        "Enable Sora video generation",
        value=False,
        help="This calls the Videos API and can cost noticeably more than text/image testing. Keep it off unless you intentionally want real motion video.",
    )
    full_sora_enabled = st.checkbox(
        "I understand: generate FULL Sora video",
        value=False,
        help="Safety gate. Full video generation renders several clips and may be slow/costly.",
    )
    sora_seconds = st.selectbox("Seconds per Sora clip", options=["4", "8", "12", "16", "20"], index=0)
    sora_size = st.selectbox("Sora size", options=["1280x720", "720x1280"], index=0)
    max_sora_shots = st.slider(
        "Maximum Sora shots to render",
        min_value=1,
        max_value=6,
        value=6,
        help="Use 1 or 2 for tests; 6 renders the full current storyboard.",
    )
    use_mock = st.checkbox(
        "Use built-in mock mode",
        value=False,
        help="Useful before spending API credits or while testing the UI. In mock mode, the app uses the sample story package and creates placeholder images.",
    )
    character_lock_notes = st.text_area(
        "Character locking requirements",
        value=(
            "Milo the kitten: small fluffy kitten with warm brown-and-cream fur, hazel eyes, soft loose curls in his forehead fur, gentle expressive face, tiny paws, optional pale blue moon-pattern neckerchief.\n"
            "Tooth Fairy: very dainty, blue eyes, short white hair, blue gown embroidered with tiny teeth, delicate magical presence.\n"
            "Keep these traits consistent across all images and video clips."
        ),
        height=140,
        help="These notes are appended to the premise so the structured story package and character-lock prompts respect your intended recurring character design.",
    )
    st.markdown("---")
    st.write("Pipeline")
    st.code(
        "Premise → character-locked story package → reference cards → scene images → animatic MP4 → optional full Sora video",
        language="text",
    )
    st.write("Recommended order")
    st.markdown(
        "1. **Generate story package**\n"
        "2. **Generate character reference cards**\n"
        "3. **Generate scene images**\n"
        "4. **Assemble MP4 from current run**\n"
        "5. Optional: **Generate full real Sora video**"
    )

premise = st.text_area("Story premise", value=SAMPLE_PREMISE, height=150)

if "story_package" not in st.session_state:
    st.session_state.story_package = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "run_dir" not in st.session_state:
    st.session_state.run_dir = None
if "character_reference_paths" not in st.session_state:
    st.session_state.character_reference_paths = {}
if "image_paths" not in st.session_state:
    st.session_state.image_paths = []
if "sora_video_path" not in st.session_state:
    st.session_state.sora_video_path = None
if "sora_clip_paths" not in st.session_state:
    st.session_state.sora_clip_paths = []
if "sora_prompt" not in st.session_state:
    st.session_state.sora_prompt = None

col_a, col_b, col_c, col_d, col_e = st.columns([1.2, 1.15, 1.05, 1.25, 1.35])
with col_a:
    generate_clicked = st.button("Step 1 — Generate story package", type="primary")
with col_b:
    refs_clicked = st.button("Step 2 — Generate character reference cards")
with col_c:
    image_clicked = st.button("Step 3 — Generate scene images")
with col_d:
    video_clicked = st.button("Step 4 — Assemble MP4 from current run")
with col_e:
    sora_clicked = st.button("Step 5 — Generate full real Sora video")

pipeline = MoonlitPipeline(model=model, image_model=image_model, video_model=video_model)

if generate_clicked:
    with st.spinner("Generating structured short-drama package..."):
        run_dir = pipeline.create_run_dir()
        full_premise = premise + "\n\nCharacter locking requirements:\n" + character_lock_notes
        package = pipeline.generate(premise=full_premise, use_mock=use_mock)
        pipeline.save_package(package, output_dir=run_dir)
        st.session_state.story_package = package
        st.session_state.video_path = None
        st.session_state.run_dir = str(run_dir)
        st.session_state.character_reference_paths = {}
        st.session_state.image_paths = []
        st.session_state.sora_video_path = None
        st.session_state.sora_clip_paths = []
        st.session_state.sora_prompt = None
    st.success(f"Story package generated. Current run folder: {st.session_state.run_dir}")

package = st.session_state.story_package
run_dir = Path(st.session_state.run_dir) if st.session_state.run_dir else None

if package:
    st.caption(f"Current run: `{run_dir}`" if run_dir else "")
    max_shot_for_sora = max(1, len(package.video_prompts))
    st.caption(f"Full Sora mode will render up to {min(max_sora_shots, max_shot_for_sora)} shot(s) from the storyboard.")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "Story brief", "Script", "Storyboard", "Visual prompts", "Continuity bible", "Character lock cards", "Generated images", "Continuity report", "Edit plan", "Real video", "Exports"
    ])

    with tab1:
        st.subheader(package.brief.title)
        st.write(package.brief.logline)
        cols = st.columns(4)
        cols[0].metric("Duration", f"{package.brief.target_duration_seconds}s")
        cols[1].metric("Genre", package.brief.genre)
        cols[2].metric("Tone", package.brief.tone)
        cols[3].metric("Audience", package.brief.audience)
        st.markdown("### Emotional theme")
        st.info(package.brief.emotional_theme)
        st.markdown("### Characters")
        for c in package.characters:
            with st.expander(c.name, expanded=True):
                st.write(f"**Role:** {c.role}")
                st.write(c.description)
                st.write(f"**Arc:** {c.emotional_arc}")
                st.write(f"**Visual notes:** {c.visual_notes}")

    with tab2:
        for s in package.scenes:
            with st.expander(f"Scene {s.scene_number}: {s.title}", expanded=True):
                st.write(f"**Duration:** {s.duration_seconds}s")
                st.write(f"**Location:** {s.location}")
                st.write(f"**Action:** {s.action}")
                st.write(f"**Emotional beat:** {s.emotional_beat}")
                st.write(f"**Caption/dialogue:** {s.dialogue_or_caption}")
                st.write(f"**Camera:** {s.camera_direction}")
                st.write(f"**Sound:** {s.sound_or_music_notes}")

    with tab3:
        for shot in package.storyboard:
            st.markdown(f"### Shot {shot.shot_number} — Scene {shot.scene_number}")
            st.write(f"**Type:** {shot.shot_type}")
            st.write(f"**Visual:** {shot.visual_description}")
            st.write(f"**Movement:** {shot.camera_movement}")
            st.write(f"**Lighting:** {shot.lighting}")
            st.write(f"**Transition:** {shot.transition}")

    with tab4:
        st.markdown("### Visual style bible")
        st.json(package.visual_style_bible.model_dump())
        st.markdown("### Generation prompts")
        for prompt in package.video_prompts:
            with st.expander(f"Shot {prompt.shot_number}"):
                st.write(prompt.prompt)
                if prompt.negative_prompt:
                    st.caption(f"Negative prompt: {prompt.negative_prompt}")

    with tab5:
        st.markdown("### Character Continuity Bible")
        st.write(
            "v0.7 generates stable identity profiles and shot-level continuity memory. "
            "These blocks are reused inside image and Sora prompts to improve character consistency."
        )
        for profile in package.character_continuity_profiles:
            with st.expander(profile.name, expanded=True):
                st.write(f"**Stable identity:** {profile.stable_identity}")
                st.write(f"**Face/body:** {profile.face_and_body}")
                st.write(f"**Hair/eyes:** {profile.hair_and_eyes}")
                st.write(f"**Clothing/props:** {profile.clothing_and_props}")
                st.write(f"**Expression/movement:** {profile.expression_and_movement}")
                st.markdown("**Do not change:**")
                for rule in profile.do_not_change:
                    st.markdown(f"- {rule}")

        st.markdown("### Global Continuity Lock")
        st.json(package.global_continuity_lock.model_dump())

        st.markdown("### Shot-by-shot continuity memory")
        for note in package.shot_continuity_notes:
            with st.expander(f"Shot {note.shot_number}"):
                st.write(f"**Characters present:** {', '.join(note.characters_present) or 'none visible'}")
                st.write(f"**From previous shot:** {note.continuity_from_previous_shot}")
                st.write(f"**Required character details:** {note.required_character_details}")
                st.write(f"**Props/costume state:** {note.props_and_costume_state}")
                st.write(f"**Environment state:** {note.environment_state}")
                st.warning(f"Consistency risk: {note.consistency_risk}")
                st.info(f"Prompt anchor: {note.prompt_anchor}")

    with tab6:
        st.markdown("### Character reference cards")
        st.write(
            "Generate reusable character lock cards first. These reference assets are then reused to guide scene image generation for stronger identity consistency."
        )
        ref_paths = st.session_state.character_reference_paths or {}
        if ref_paths:
            cols = st.columns(2)
            for idx, (name, path_str) in enumerate(ref_paths.items()):
                with cols[idx % 2]:
                    st.image(path_str, caption=name, use_container_width=True)
                    path = Path(path_str)
                    if path.exists():
                        st.download_button(
                            f"Download {name} reference",
                            path.read_bytes(),
                            file_name=path.name,
                            mime="image/png",
                            key=f"download_ref_{idx}",
                        )
        else:
            st.info("No character reference cards generated yet. Click Step 2 first.")

    with tab7:
        st.markdown("### Generated / assembled visual frames")

        raw_image_paths = []
        frame_paths = []

        if run_dir:
            images_dir = run_dir / "images"
            frames_dir = run_dir / "frames"

            if images_dir.exists():
                raw_image_paths = sorted(images_dir.glob("shot_*.png"))

            if frames_dir.exists():
                frame_paths = sorted(frames_dir.glob("*.jpg"))

        if not raw_image_paths and st.session_state.image_paths:
            raw_image_paths = [Path(p) for p in st.session_state.image_paths]

        if raw_image_paths:
            st.success(f"{len(raw_image_paths)} raw generated scene images found.")
            st.markdown("#### Raw generated images")
            image_cols = st.columns(2)
            for idx, img_path in enumerate(raw_image_paths):
                with image_cols[idx % 2]:
                    st.image(str(img_path), caption=img_path.name, use_container_width=True)

        if frame_paths:
            st.success(f"{len(frame_paths)} assembled MP4 frames found.")
            st.markdown("#### MP4-ready frames")
            frame_cols = st.columns(2)
            for idx, frame_path in enumerate(frame_paths):
                with frame_cols[idx % 2]:
                    st.image(str(frame_path), caption=frame_path.name, use_container_width=True)

        if not raw_image_paths and not frame_paths:
            st.warning("No images or assembled frames found yet. Click **Step 3 — Generate scene images**, then **Step 4 — Assemble MP4**.")

    with tab8:
        st.markdown("### Strengths")
        for item in package.continuity_report.strengths:
            st.success(item)
        st.markdown("### Risks")
        for item in package.continuity_report.risks:
            st.warning(item)
        st.markdown("### Fixes applied")
        for item in package.continuity_report.fixes_applied:
            st.info(item)
        st.markdown("### Final assessment")
        st.write(package.continuity_report.final_assessment)

    with tab9:
        for e in package.edit_decisions:
            st.markdown(f"**{e.order}. Scene {e.scene_number}, Shot {e.shot_number} — {e.duration_seconds}s**")
            st.write(e.on_screen_text)
            st.caption(f"Transition: {e.transition} · Audio: {e.audio_note}")
        st.markdown("### Token budget")
        st.json(package.token_budget.model_dump())

    with tab10:
        st.markdown("### Optional full real motion video")
        st.write(
            "This step uses the OpenAI Videos API / Sora to render one real motion clip per storyboard shot, "
            "then concatenates the clips into a full MP4. Use 4-second clips and 1–2 shots first to control cost and latency."
        )
        if st.session_state.sora_clip_paths:
            st.markdown("#### Individual Sora clips")
            for clip_path in st.session_state.sora_clip_paths:
                clip_path = Path(clip_path)
                if clip_path.exists():
                    st.video(str(clip_path))
                    st.caption(str(clip_path))
        if st.session_state.sora_video_path:
            sora_path = Path(st.session_state.sora_video_path)
            if sora_path.exists():
                st.success(f"Full Sora video created: {sora_path}")
                st.video(str(sora_path))
                st.download_button("Download full Sora MP4", sora_path.read_bytes(), file_name=sora_path.name, mime="video/mp4", key="download_full_sora_mp4_tab")
        else:
            st.info("No full Sora video generated yet. Enable both Sora safety toggles in the sidebar, then click Step 5.")

    with tab11:
        json_data = package.model_dump_json(indent=2)
        md_data = package.to_markdown()
        st.download_button("Download story_package.json", json_data, file_name="story_package.json")
        st.download_button("Download story_package.md", md_data, file_name="story_package.md")
        if run_dir and run_dir.exists():
            st.caption(f"Run folder on disk: {run_dir}")

if refs_clicked:
    if not package or not run_dir:
        st.error("Generate a story package first.")
    else:
        with st.spinner("Generating character reference cards..."):
            ref_paths = pipeline.generate_character_references(package, output_dir=run_dir, use_mock=use_mock)
            st.session_state.character_reference_paths = {name: str(path) for name, path in ref_paths.items()}
        st.success(f"Generated {len(st.session_state.character_reference_paths)} character reference cards.")

if image_clicked:
    if not package or not run_dir:
        st.error("Generate a story package first.")
    else:
        with st.spinner("Generating scene images..."):
            ref_paths = {name: Path(path) for name, path in st.session_state.character_reference_paths.items()}
            if not ref_paths:
                auto_refs = pipeline.generate_character_references(package, output_dir=run_dir, use_mock=use_mock)
                st.session_state.character_reference_paths = {name: str(path) for name, path in auto_refs.items()}
                ref_paths = auto_refs
            image_paths = pipeline.generate_images(package, output_dir=run_dir, use_mock=use_mock, character_reference_paths=ref_paths)
            st.session_state.image_paths = [str(p) for p in image_paths]
        st.success(f"Generated {len(st.session_state.image_paths)} scene images.")

if video_clicked:
    if not package or not run_dir:
        st.error("Generate a story package first.")
    else:
        with st.spinner("Assembling visual animatic MP4..."):
            video_path = pipeline.create_video(package, output_dir=run_dir)
            st.session_state.video_path = str(video_path)
        st.success(f"MP4 created: {video_path}")


if sora_clicked:
    if not package or not run_dir:
        st.error("Generate a story package first.")
    elif not sora_enabled or not full_sora_enabled:
        st.error("Enable both Sora safety toggles in the sidebar first. This prevents accidental paid full-video calls.")
    else:
        st.warning(
            f"Starting full Sora generation: up to {max_sora_shots} clip(s), {sora_seconds}s each. "
            "Character locking is strongest in the reference-card + scene-image pipeline; Sora still relies primarily on continuity-aware prompts and may drift slightly."
        )
        try:
            with st.spinner("Generating full Sora video. This may take a long time..."):
                result = pipeline.generate_full_real_video(
                    package,
                    output_dir=run_dir,
                    model=video_model,
                    size=sora_size,
                    seconds_per_clip=sora_seconds,
                    max_shots=max_sora_shots,
                )
                st.session_state.sora_clip_paths = [str(p) for p in result["clips"]]
                st.session_state.sora_video_path = str(result["full_video"])
            st.success(f"Full Sora video created: {st.session_state.sora_video_path}")
        except Exception as exc:
            msg = str(exc)
            lowered = msg.lower()
            if "moderation" in lowered or "blocked" in lowered:
                st.error("Sora blocked this video prompt via moderation. The app now uses a safer prompt layer, but a specific shot may still need softer wording. Check the latest `sora_prompt_shot_XX.txt` file in your run folder.")
            elif "billing hard limit" in lowered or "billing_hard_limit_reached" in lowered:
                st.error("OpenAI billing hard limit reached. Raise your API budget or wait for reset before running Sora again.")
            else:
                st.error(f"Sora generation failed: {msg}")

if st.session_state.video_path:
    path = Path(st.session_state.video_path)
    if path.exists():
        st.markdown("### Current animatic MP4")
        st.video(str(path))
        st.download_button("Download animatic MP4", path.read_bytes(), file_name=path.name, mime="video/mp4", key="download_animatic_mp4_current")

if st.session_state.sora_video_path:
    sora_path = Path(st.session_state.sora_video_path)
    if sora_path.exists():
        st.markdown("### Current full real Sora video")
        st.video(str(sora_path))
        st.download_button("Download full Sora MP4", sora_path.read_bytes(), file_name=sora_path.name, mime="video/mp4", key="download_full_sora_mp4_bottom")
