"""Tests for the download helper module."""

from __future__ import annotations

from pathlib import Path

import pytest
import responses

from civitcli.config import DownloadPaths
from civitcli.downloader import DownloadError, ResourceType, download_resource


@pytest.fixture()
def download_paths(tmp_path: Path) -> DownloadPaths:
    return DownloadPaths(
        checkpoints=tmp_path / "checkpoints",
        loras=tmp_path / "loras",
        embeddings=tmp_path / "embeddings",
    )


@responses.activate
def test_download_resource_saves_file_and_detects_type(download_paths: DownloadPaths) -> None:
    url = "https://example.com/loras/cool-lora.safetensors"
    responses.add(responses.GET, url, body=b"contents", status=200)

    result = download_resource(url, paths=download_paths)

    assert result.resource_type is ResourceType.LORA
    assert result.path.exists()
    assert result.path.read_bytes() == b"contents"
    assert result.path.parent == download_paths.loras


@responses.activate
def test_download_resource_includes_auth_header(monkeypatch: pytest.MonkeyPatch, download_paths: DownloadPaths) -> None:
    url = "https://example.com/models/cool-model.safetensors"
    monkeypatch.setenv("CIVITAI_API", "secret-token")

    responses.add(responses.GET, url, body=b"data", status=200)

    download_resource(url, paths=download_paths)

    assert responses.calls[0].request.headers["CIVITAI_API"] == "secret-token"


@responses.activate
def test_download_resource_raises_for_http_error(download_paths: DownloadPaths) -> None:
    url = "https://example.com/embeddings/token.pt"
    responses.add(responses.GET, url, status=404)

    with pytest.raises(DownloadError):
        download_resource(url, paths=download_paths)
