"""Download helpers for Civitai resources."""

from __future__ import annotations

from pathlib import Path
from typing import Optional


class DownloadError(RuntimeError):
    """Raised when a download fails."""


def download_resource(url: str, *, session: Optional[object] = None) -> Path:  # pragma: no cover - stub
    """Download a resource from ``url``.

    This stub will be implemented in Milestone 1. It currently raises
    :class:`NotImplementedError` to signal that the functionality is not yet
    available.
    """

    raise NotImplementedError("Download functionality will be delivered in Milestone 1.")
