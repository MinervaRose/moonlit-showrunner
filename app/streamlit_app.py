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
st.caption("An AI-assisted short-drama pipeline from premise to visual animatic MP4")

st.info(
    "**Version note:** v0.3.1 generates a structured story package, can generate stylized 3D scene images, and assembles a visual animatic MP4. "
    "It does **not** yet create true AI-generated motion video clips. The final MP4 is assembled from still images or fallback scene cards."
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenAI text model", value=st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini"))
    image_model = st.text_input("OpenAI image model", value=st.secrets.get("OPENAI_IMAGE_MODEL", "gpt-image-1"))
    use_mock = st.checkbox(
        "Use built-in mock mode",
        value=False,
        help="Useful before spending API credits or while testing the UI. In mock mode, the app uses the sample story package and creates placeholder images.",
    )
    st.markdown("---")
    st.write("Pipeline")
    st.code(
        "Premise → story package → scene images → visual animatic MP4",
        language="text",
    )
    st.write("Recommended order")
    st.markdown(
        "1. **Generate story package**\n"
        "2. **Generate scene images**\n"
        "3. **Assemble MP4 from current run**"
    )

premise = st.text_area("Story premise", value=SAMPLE_PREMISE, height=150)

if "story_package" not in st.session_state:
    st.session_state.story_package = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "run_dir" not in st.session_state:
    st.session_state.run_dir = None
if "image_paths" not in st.session_state:
    st.session_state.image_paths = []

col_a, col_b, col_c = st.columns([1.25, 1.1, 1.3])
with col_a:
    generate_clicked = st.button("Step 1 — Generate story package", type="primary")
with col_b:
    image_clicked = st.button("Step 2 — Generate scene images")
with col_c:
    video_clicked = st.button("Step 3 — Assemble MP4 from current run")

pipeline = MoonlitPipeline(model=model, image_model=image_model)

if generate_clicked:
    with st.spinner("Generating structured short-drama package..."):
        run_dir = pipeline.create_run_dir()
        package = pipeline.generate(premise=premise, use_mock=use_mock)
        pipeline.save_package(package, output_dir=run_dir)
        st.session_state.story_package = package
        st.session_state.video_path = None
        st.session_state.run_dir = str(run_dir)
        st.session_state.image_paths = []
    st.success(f"Story package generated. Current run folder: {st.session_state.run_dir}")

package = st.session_state.story_package
run_dir = Path(st.session_state.run_dir) if st.session_state.run_dir else None

if package:
    st.caption(f"Current run: `{run_dir}`" if run_dir else "")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Story brief", "Script", "Storyboard", "Visual prompts", "Generated images", "Continuity", "Edit plan", "Exports"
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
            st.warning("No images or assembled frames found yet. Click **Step 2 — Generate scene images**, then **Step 3 — Assemble MP4**.")

    with tab6:
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

    with tab7:
        for e in package.edit_decisions:
            st.markdown(f"**{e.order}. Scene {e.scene_number}, Shot {e.shot_number} — {e.duration_seconds}s**")
            st.write(e.on_screen_text)
            st.caption(f"Transition: {e.transition} · Audio: {e.audio_note}")
        st.markdown("### Token budget")
        st.json(package.token_budget.model_dump())

    with tab8:
        json_data = package.model_dump_json(indent=2)
        md_data = package.to_markdown()
        st.download_button("Download story_package.json", json_data, file_name="story_package.json")
        st.download_button("Download story_package.md", md_data, file_name="story_package.md")
        if run_dir and run_dir.exists():
            st.caption(f"Run folder on disk: {run_dir}")

if image_clicked:
    if not package or not run_dir:
        st.error("Generate a story package first.")
    else:
        with st.spinner("Generating scene images..."):
            image_paths = pipeline.generate_images(package, output_dir=run_dir, use_mock=use_mock)
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

if st.session_state.video_path:
    path = Path(st.session_state.video_path)
    if path.exists():
        st.markdown("### Current MP4")
        st.video(str(path))
        st.download_button("Download MP4", path.read_bytes(), file_name=path.name, mime="video/mp4")
