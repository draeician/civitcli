"""Smoke tests for the civitcli command-line interface."""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

import pytest

from civitcli import cli as cli_module
from civitcli.downloader import DownloadError


def test_cli_help() -> None:
    """The CLI should respond to ``--help`` without error."""

    result = subprocess.run(
        [sys.executable, "-m", "civitcli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()


def test_cli_download_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)

    def fake_download(url: str):
        class _Result:
            filename = "model.safetensors"
            path = tmp_path / "model.safetensors"

        return _Result()

    monkeypatch.setattr(cli_module, "download_resource", fake_download)

    exit_code = cli_module.main(["-v", "--download", "https://example.com/model.safetensors"])

    assert exit_code == 0
    assert "Downloaded model.safetensors" in caplog.text


def test_cli_download_failure(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.ERROR)

    def fake_download(url: str):
        raise DownloadError("boom")

    monkeypatch.setattr(cli_module, "download_resource", fake_download)

    exit_code = cli_module.main(["--download", "https://example.com/model.safetensors"])

    assert exit_code == 1
    assert "boom" in caplog.text
