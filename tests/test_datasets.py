"""Tests for datasets registry."""

from gtra.datasets import DATASET_BY_ID, DATASETS


def test_all_datasets_have_required_keys():
    required = {"id", "name", "source_url", "bulk_available", "description", "page"}
    for ds in DATASETS:
        missing = required - ds.keys()
        assert not missing, f"{ds['id']} missing keys: {missing}"


def test_ids_are_unique():
    ids = [d["id"] for d in DATASETS]
    assert len(ids) == len(set(ids))


def test_bulk_available_have_bulk_url():
    for ds in DATASETS:
        if ds["bulk_available"]:
            assert ds.get("bulk_url"), f"{ds['id']} bulk_available=True but no bulk_url"


def test_dataset_by_id_index():
    assert set(DATASET_BY_ID.keys()) == {d["id"] for d in DATASETS}


def test_copyright_dataset():
    ds = DATASET_BY_ID["copyright"]
    assert ds["bulk_available"] is True
    assert "storage.googleapis.com" in ds["bulk_url"]


def test_non_bulk_datasets():
    non_bulk = [d for d in DATASETS if not d["bulk_available"]]
    assert len(non_bulk) >= 6


def test_pages_are_html_files():
    for ds in DATASETS:
        assert ds["page"].endswith(".html"), f"{ds['id']} page must end with .html"
