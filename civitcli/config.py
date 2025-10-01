"""Configuration helpers for :mod:`civitcli`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Default paths sourced from the MVP PRD.
DEFAULT_MODELS_DIR = Path("/opt/md2/backup/civitai/models")
DEFAULT_LORAS_DIR = DEFAULT_MODELS_DIR / "loras"
DEFAULT_EMBEDDINGS_DIR = DEFAULT_MODELS_DIR / "embeddings"


@dataclass(frozen=True)
class DownloadPaths:
    """Container for download target directories."""

    checkpoints: Path = DEFAULT_MODELS_DIR
    loras: Path = DEFAULT_LORAS_DIR
    embeddings: Path = DEFAULT_EMBEDDINGS_DIR


def load_download_paths() -> DownloadPaths:
    """Return the download paths using default configuration.

    Future milestones will extend this function to read from environment
    variables and configuration files.
    """

    return DownloadPaths()
