from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.pipeline import run_full_pipeline
from app.sample_data import SAMPLE_PREMISE


if __name__ == "__main__":
    result = run_full_pipeline(SAMPLE_PREMISE, use_mock=True)
    print("Generated files:")
    print(f"- run_dir: {result['run_dir']}")
    for label, path in result["files"].items():
        print(f"- {label}: {path}")
    for image in result["images"]:
        print(f"- image: {image}")
    print(f"- video: {result['video']}")
