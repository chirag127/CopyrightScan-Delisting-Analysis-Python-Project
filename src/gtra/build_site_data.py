"""Export analysis results as JSON into docs/data/ for the static site."""

import json
from pathlib import Path

from .analyze import run_analysis
from .datasets import DATASETS

DATA_DIR = Path(__file__).parent.parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"
SITE_DATA_DIR = Path(__file__).parent.parent.parent / "docs" / "data"


def build(
    data_dir: Path = DATA_DIR,
    out_dir: Path = OUTPUT_DIR,
    site_dir: Path = SITE_DATA_DIR,
) -> None:
    site_dir.mkdir(parents=True, exist_ok=True)

    manifest = {"datasets": []}

    for ds in DATASETS:
        did = ds["id"]
        try:
            result = run_analysis(did, data_dir, out_dir)
        except Exception as exc:
            result = {"error": str(exc)}

        payload = {
            "id": did,
            "name": ds["name"],
            "source_url": ds["source_url"],
            "bulk_available": ds["bulk_available"],
            "description": ds["description"],
            "page": ds["page"],
            "data": result,
        }
        out_path = site_dir / f"{did}.json"
        out_path.write_text(json.dumps(payload, indent=2, default=str))
        print(f"  wrote {out_path}")
        manifest["datasets"].append({"id": did, "name": ds["name"], "page": ds["page"]})

    (site_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"  wrote {site_dir / 'manifest.json'}")


if __name__ == "__main__":
    build()
