"""Download and extract Google Web Search Copyright Removals dataset."""

import io
import zipfile
from pathlib import Path

import requests

DATASET_URL = (
    "https://storage.googleapis.com/transparencyreport/"
    "google-websearch-copyright-removals.zip"
)
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def download_dataset(data_dir: Path = DATA_DIR, force: bool = False) -> Path:
    """Download and extract the dataset; skip if already present."""
    data_dir.mkdir(parents=True, exist_ok=True)
    zip_path = data_dir / "google-websearch-copyright-removals.zip"

    if not force and any(data_dir.glob("*.csv")):
        print(f"Dataset already in {data_dir}; skipping download.")
        return data_dir

    print("Downloading dataset (~80 MB)…")
    resp = requests.get(DATASET_URL, timeout=120)
    resp.raise_for_status()

    zip_path.write_bytes(resp.content)
    print(f"Saved zip: {zip_path}")

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        zf.extractall(data_dir)
        print(f"Extracted: {zf.namelist()}")

    return data_dir
