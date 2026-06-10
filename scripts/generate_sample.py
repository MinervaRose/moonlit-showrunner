from __future__ import annotations

from pathlib import Path
import sys

# Allow running from repository root without installing as a package.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.pipeline import run_full_pipeline
from app.sample_data import SAMPLE_PREMISE


if __name__ == "__main__":
    result = run_full_pipeline(SAMPLE_PREMISE, use_mock=True, output_dir=ROOT / "outputs")
    print("Generated files:")
    for label, path in result["files"].items():
        print(f"- {label}: {path}")
    print(f"- video: {result['video']}")
