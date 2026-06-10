from __future__ import annotations

import json
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
st.caption("An AI-assisted short-drama pipeline from premise to MP4")

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenAI model", value=st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini"))
    use_mock = st.checkbox("Use built-in mock package", value=False, help="Useful before adding an API key or while testing the UI.")
    st.markdown("---")
    st.write("Pipeline:")
    st.code("Premise → story → storyboard → prompts → edit plan → MP4", language="text")

premise = st.text_area("Story premise", value=SAMPLE_PREMISE, height=150)

if "story_package" not in st.session_state:
    st.session_state.story_package = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None

col_a, col_b, col_c = st.columns([1, 1, 2])
with col_a:
    generate_clicked = st.button("Generate story package", type="primary")
with col_b:
    video_clicked = st.button("Assemble MP4")

pipeline = MoonlitPipeline(model=model)

if generate_clicked:
    with st.spinner("Generating structured short-drama package..."):
        package = pipeline.generate(premise=premise, use_mock=use_mock)
        pipeline.save_package(package)
        st.session_state.story_package = package
        st.session_state.video_path = None
    st.success("Story package generated.")

package = st.session_state.story_package

if package:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Story brief", "Script", "Storyboard", "Visual prompts", "Continuity", "Edit plan", "Exports"
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
        st.write(package.visual_style_bible.model_dump())
        st.markdown("### Generation prompts")
        for prompt in package.video_prompts:
            with st.expander(f"Shot {prompt.shot_number}"):
                st.write(prompt.prompt)
                if prompt.negative_prompt:
                    st.caption(f"Negative prompt: {prompt.negative_prompt}")

    with tab5:
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

    with tab6:
        for e in package.edit_decisions:
            st.markdown(f"**{e.order}. Scene {e.scene_number}, Shot {e.shot_number} — {e.duration_seconds}s**")
            st.write(e.on_screen_text)
            st.caption(f"Transition: {e.transition} · Audio: {e.audio_note}")
        st.markdown("### Token budget")
        st.json(package.token_budget.model_dump())

    with tab7:
        json_data = package.model_dump_json(indent=2)
        md_data = package.to_markdown()
        st.download_button("Download story_package.json", json_data, file_name="story_package.json")
        st.download_button("Download story_package.md", md_data, file_name="story_package.md")

if video_clicked:
    if not package:
        st.error("Generate a story package first.")
    else:
        with st.spinner("Assembling MP4..."):
            video_path = pipeline.create_video(package)
            st.session_state.video_path = str(video_path)
        st.success(f"MP4 created: {video_path}")

if st.session_state.video_path:
    path = Path(st.session_state.video_path)
    if path.exists():
        st.video(str(path))
        st.download_button("Download MP4", path.read_bytes(), file_name=path.name, mime="video/mp4")
