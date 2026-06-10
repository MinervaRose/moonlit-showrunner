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
st.caption("An AI-assisted short-drama pipeline from premise to visual animatic MP4, with optional full real Sora video generation")

st.info(
    "**Version note:** v0.3.1 generates a structured story package, can generate stylized 3D scene images, and assembles a visual animatic MP4. "
    "The main MP4 is assembled from still images or fallback scene cards. v0.5 adds an optional Sora step that can generate one real motion clip per storyboard shot and concatenate them into a full MP4."
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
    st.markdown("---")
    st.write("Pipeline")
    st.code(
        "Premise → story package → scene images → animatic MP4 → optional full Sora video",
        language="text",
    )
    st.write("Recommended order")
    st.markdown(
        "1. **Generate story package**\n"
        "2. **Generate scene images**\n"
        "3. **Assemble MP4 from current run**\n"
        "4. Optional: **Generate full real Sora video**"
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
if "sora_video_path" not in st.session_state:
    st.session_state.sora_video_path = None
if "sora_clip_paths" not in st.session_state:
    st.session_state.sora_clip_paths = []
if "sora_prompt" not in st.session_state:
    st.session_state.sora_prompt = None

col_a, col_b, col_c, col_d = st.columns([1.25, 1.1, 1.3, 1.25])
with col_a:
    generate_clicked = st.button("Step 1 — Generate story package", type="primary")
with col_b:
    image_clicked = st.button("Step 2 — Generate scene images")
with col_c:
    video_clicked = st.button("Step 3 — Assemble MP4 from current run")
with col_d:
    sora_clicked = st.button("Step 4 — Generate full real Sora video")

pipeline = MoonlitPipeline(model=model, image_model=image_model, video_model=video_model)

if generate_clicked:
    with st.spinner("Generating structured short-drama package..."):
        run_dir = pipeline.create_run_dir()
        package = pipeline.generate(premise=premise, use_mock=use_mock)
        pipeline.save_package(package, output_dir=run_dir)
        st.session_state.story_package = package
        st.session_state.video_path = None
        st.session_state.run_dir = str(run_dir)
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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "Story brief", "Script", "Storyboard", "Visual prompts", "Generated images", "Continuity", "Edit plan", "Real video", "Exports"
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
                st.download_button("Download full Sora MP4", sora_path.read_bytes(), file_name=sora_path.name, mime="video/mp4")
        else:
            st.info("No full Sora video generated yet. Enable both Sora safety toggles in the sidebar, then click Step 4.")

    with tab9:
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


if sora_clicked:
    if not package or not run_dir:
        st.error("Generate a story package first.")
    elif not sora_enabled or not full_sora_enabled:
        st.error("Enable both Sora safety toggles in the sidebar first. This prevents accidental paid full-video calls.")
    else:
        st.warning(
            f"Starting full Sora generation: up to {max_sora_shots} clip(s), {sora_seconds}s each. "
            "This may take several minutes per clip."
        )
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

if st.session_state.video_path:
    path = Path(st.session_state.video_path)
    if path.exists():
        st.markdown("### Current animatic MP4")
        st.video(str(path))
        st.download_button("Download animatic MP4", path.read_bytes(), file_name=path.name, mime="video/mp4")

if st.session_state.sora_video_path:
    sora_path = Path(st.session_state.sora_video_path)
    if sora_path.exists():
        st.markdown("### Current full real Sora video")
        st.video(str(sora_path))
        st.download_button("Download full Sora MP4", sora_path.read_bytes(), file_name=sora_path.name, mime="video/mp4", key="download_full_sora_mp4_bottom",)
