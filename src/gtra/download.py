"""Download and cache datasets from Google Transparency Report."""

import io
import zipfile
from pathlib import Path

import requests

from .datasets import DATASET_BY_ID

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# Known bulk-downloadable dataset
_COPYRIGHT_URL = (
    "https://storage.googleapis.com/transparencyreport/"
    "google-websearch-copyright-removals.zip"
)


def _data_dir(dataset_id: str, base: Path = DATA_DIR) -> Path:
    d = base / dataset_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def download_copyright(base: Path = DATA_DIR, force: bool = False) -> Path:
    """Download and extract copyright removals CSV; skip if cached."""
    dest = _data_dir("copyright", base)
    if not force and any(dest.glob("*.csv")):
        print(f"copyright: cached in {dest}")
        return dest

    print("Downloading copyright removals dataset (~80 MB)...")
    resp = requests.get(_COPYRIGHT_URL, timeout=180)
    resp.raise_for_status()

    zip_path = dest / "google-websearch-copyright-removals.zip"
    zip_path.write_bytes(resp.content)

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        zf.extractall(dest)
        print(f"  Extracted: {zf.namelist()}")

    return dest


def download_dataset(
    dataset_id: str, base: Path = DATA_DIR, force: bool = False
) -> Path | None:
    """Download a dataset by id. Returns dest dir or None if not bulk-available."""
    ds = DATASET_BY_ID.get(dataset_id)
    if ds is None:
        raise ValueError(f"Unknown dataset: {dataset_id}")
    if not ds["bulk_available"]:
        print(f"{dataset_id}: no bulk download — see {ds['source_url']}")
        return None
    if dataset_id == "copyright":
        return download_copyright(base, force)
    raise NotImplementedError(f"bulk download not implemented for {dataset_id}")


def download_all(base: Path = DATA_DIR, force: bool = False) -> dict[str, Path | None]:
    """Attempt download for all datasets; returns {id: path_or_None}."""
    results = {}
    from .datasets import DATASETS

    for ds in DATASETS:
        results[ds["id"]] = download_dataset(ds["id"], base, force)
    return results
