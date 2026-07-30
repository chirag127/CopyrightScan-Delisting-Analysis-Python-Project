"""Smoke tests for analyze.py chart generation and build_site_data.py JSON output."""

import json
from pathlib import Path

import pandas as pd
import pytest
from gtra.analyze import analyze_copyright, analyze_stub, run_analysis
from gtra.build_site_data import build

# ---------------------------------------------------------------------------
# analyze_copyright
# ---------------------------------------------------------------------------


def _make_csv_dir(tmp_path: Path) -> Path:
    d = tmp_path / "copyright"
    d.mkdir(parents=True)
    rows = []
    for i in range(50):
        rows.append(
            {
                "Copyright Owner": f"Owner{i % 5}",
                "Reporting Organization": f"Org{i % 3}",
                "Domain": f"site{i % 8}.com",
                "Date": f"2020-0{(i % 9) + 1}-01",
                "URLs Requested To Remove": i * 10 + 5,
                "URLs Removed": i * 9,
            }
        )
    pd.DataFrame(rows).to_csv(d / "test.csv", index=False)
    return tmp_path


def test_analyze_copyright_returns_findings(tmp_path: Path):
    data_dir = _make_csv_dir(tmp_path)
    out_dir = tmp_path / "output"
    result = analyze_copyright(data_dir, out_dir)
    assert "findings" in result
    assert result["findings"]["total_records"] == 50
    assert "charts" in result
    assert len(result["charts"]) > 0


def test_analyze_copyright_saves_charts(tmp_path: Path):
    data_dir = _make_csv_dir(tmp_path)
    out_dir = tmp_path / "output"
    analyze_copyright(data_dir, out_dir)
    pngs = list(out_dir.glob("copyright_*.png"))
    assert len(pngs) >= 3


def test_analyze_copyright_missing_data_raises(tmp_path: Path):
    empty = tmp_path / "copyright"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        analyze_copyright(tmp_path, tmp_path / "output")


def test_analyze_stub_returns_known_id():
    result = analyze_stub("gov-removals")
    assert "key_facts" in result
    assert len(result["key_facts"]) >= 1


def test_analyze_stub_unknown_id():
    result = analyze_stub("totally-unknown")
    assert result == {"note": "No data available."}


def test_run_analysis_copyright(tmp_path: Path):
    data_dir = _make_csv_dir(tmp_path)
    result = run_analysis("copyright", data_dir, tmp_path / "output")
    assert "findings" in result


def test_run_analysis_stub(tmp_path: Path):
    result = run_analysis("gov-removals", tmp_path / "data", tmp_path / "output")
    assert "key_facts" in result


# ---------------------------------------------------------------------------
# build_site_data
# ---------------------------------------------------------------------------


def test_build_site_data_creates_json(tmp_path: Path):
    data_dir = _make_csv_dir(tmp_path)
    out_dir = tmp_path / "output"
    site_dir = tmp_path / "site_data"

    build(data_dir, out_dir, site_dir)

    manifest_path = site_dir / "manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    assert "datasets" in manifest
    ids_in_manifest = [d["id"] for d in manifest["datasets"]]
    assert "copyright" in ids_in_manifest
    assert "gov-removals" in ids_in_manifest


def test_build_site_data_json_schema(tmp_path: Path):
    data_dir = _make_csv_dir(tmp_path)
    site_dir = tmp_path / "site_data"
    build(data_dir, tmp_path / "output", site_dir)

    copyright_json = json.loads((site_dir / "copyright.json").read_text())
    assert copyright_json["id"] == "copyright"
    assert copyright_json["bulk_available"] is True
    assert "data" in copyright_json


def test_build_creates_all_dataset_jsons(tmp_path: Path):
    from gtra.datasets import DATASETS

    data_dir = _make_csv_dir(tmp_path)
    site_dir = tmp_path / "site_data"
    build(data_dir, tmp_path / "output", site_dir)

    for ds in DATASETS:
        assert (site_dir / f"{ds['id']}.json").exists(), f"missing {ds['id']}.json"
