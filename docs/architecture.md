# Architecture

Moonlit Showrunner is organized as a lightweight agentic production pipeline.

## Core flow

1. The user enters a short premise in the Streamlit interface.
2. The pipeline sends a structured prompt to the OpenAI API.
3. The model returns a JSON story package matching the project schema.
4. The app validates the package with Pydantic.
5. The app displays story, script, storyboard, visual direction, continuity report, and edit plan.
6. The video assembler creates title cards and scene cards using Pillow.
7. MoviePy assembles those cards into a short MP4 with timing based on the edit plan.

## Main modules

- `app/openai_client.py`: OpenAI API wrapper and structured JSON generation.
- `app/schemas.py`: Pydantic models for story packages.
- `app/pipeline.py`: High-level orchestration.
- `app/video/assemble_mp4.py`: MP4 generation.
- `app/video/make_cards.py`: Still frame/title card generation.
- `app/streamlit_app.py`: User interface.

## Design principle

The project intentionally separates the **showrunner brain** from the **video assembly layer**. This makes the prototype easy to extend later with image generation, video generation, voiceover, music, or deployment.
