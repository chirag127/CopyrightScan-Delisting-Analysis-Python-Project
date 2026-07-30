"""Tests for download.py caching logic (mocked HTTP)."""

import io
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from gtra.download import download_copyright, download_dataset


def _make_zip(filename: str = "data.csv", content: str = "col1,col2\na,b\n") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(filename, content)
    return buf.getvalue()


@pytest.fixture()
def tmp_data(tmp_path: Path) -> Path:
    return tmp_path / "data"


def test_download_copyright_skips_when_cached(tmp_data: Path, capsys):
    dest = tmp_data / "copyright"
    dest.mkdir(parents=True)
    (dest / "existing.csv").write_text("col\nval\n")

    with patch("gtra.download.requests.get") as mock_get:
        result = download_copyright(tmp_data)
        mock_get.assert_not_called()

    assert result == dest
    captured = capsys.readouterr()
    assert "cached" in captured.out


def test_download_copyright_fetches_when_missing(tmp_data: Path):
    zip_bytes = _make_zip("copyright.csv", "owner,domain\nAcme,example.com\n")
    mock_resp = MagicMock()
    mock_resp.content = zip_bytes
    mock_resp.raise_for_status = MagicMock()

    with patch("gtra.download.requests.get", return_value=mock_resp) as mock_get:
        result = download_copyright(tmp_data)
        mock_get.assert_called_once()

    assert result == tmp_data / "copyright"
    assert (result / "copyright.csv").exists()


def test_download_copyright_force_refetch(tmp_data: Path):
    dest = tmp_data / "copyright"
    dest.mkdir(parents=True)
    (dest / "old.csv").write_text("stale\n")

    zip_bytes = _make_zip("new.csv", "fresh\n")
    mock_resp = MagicMock()
    mock_resp.content = zip_bytes
    mock_resp.raise_for_status = MagicMock()

    with patch("gtra.download.requests.get", return_value=mock_resp) as mock_get:
        download_copyright(tmp_data, force=True)
        mock_get.assert_called_once()

    assert (dest / "new.csv").exists()


def test_download_dataset_unknown_raises():
    with pytest.raises(ValueError, match="Unknown dataset"):
        download_dataset("nonexistent-id")


def test_download_dataset_non_bulk_returns_none(tmp_data: Path, capsys):
    result = download_dataset("gov-removals", tmp_data)
    assert result is None
    captured = capsys.readouterr()
    assert "no bulk download" in captured.out


def test_download_dataset_copyright_delegates(tmp_data: Path):
    dest = tmp_data / "copyright"
    dest.mkdir(parents=True)
    (dest / "cached.csv").write_text("x\n")

    result = download_dataset("copyright", tmp_data)
    assert result == dest
