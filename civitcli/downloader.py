"""Download helpers for Civitai resources."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

import requests

from .config import DownloadPaths, load_download_paths

__all__ = ["DownloadError", "DownloadResult", "ResourceType", "download_resource"]


class DownloadError(RuntimeError):
    """Raised when a download fails."""


class ResourceType(str, Enum):
    """Known resource categories supported by the downloader."""

    CHECKPOINT = "checkpoints"
    LORA = "loras"
    EMBEDDING = "embeddings"


@dataclass(frozen=True)
class DownloadResult:
    """Summary of a completed download."""

    url: str
    path: Path
    resource_type: ResourceType
    filename: str
    content_type: Optional[str] = None


def download_resource(
    url: str,
    *,
    session: Optional[requests.Session] = None,
    paths: Optional[DownloadPaths] = None,
    chunk_size: int = 1024 * 1024,
) -> DownloadResult:
    """Download a resource from ``url`` and return the saved path."""

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise DownloadError(f"Invalid URL provided: {url!r}")

    close_session = False
    if session is None:
        session = requests.Session()
        close_session = True

    headers = {}
    token = os.environ.get("CIVITAI_API")
    if token:
        headers["CIVITAI_API"] = token

    try:
        response = session.get(url, stream=True, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - exercised via tests
        if close_session:
            session.close()
        raise DownloadError(f"Failed to download resource: {exc}") from exc

    filename = _resolve_filename(parsed.path, response.headers.get("Content-Disposition"))
    resource_type = _infer_resource_type(parsed.path, filename)

    target_paths = paths or load_download_paths()
    destination_dir = _destination_for_type(target_paths, resource_type)
    destination_dir.mkdir(parents=True, exist_ok=True)

    destination = destination_dir / filename
    try:
        _write_to_disk(response, destination, chunk_size=chunk_size)
    finally:
        response.close()
        if close_session:
            session.close()

    return DownloadResult(
        url=url,
        path=destination,
        resource_type=resource_type,
        filename=filename,
        content_type=response.headers.get("Content-Type"),
    )


def _write_to_disk(response: requests.Response, destination: Path, *, chunk_size: int) -> None:
    """Persist the streamed response to ``destination``."""

    with destination.open("wb") as file_obj:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if not chunk:
                continue
            file_obj.write(chunk)


def _destination_for_type(paths: DownloadPaths, resource_type: ResourceType) -> Path:
    """Return the target directory for the given ``resource_type``."""

    if resource_type is ResourceType.CHECKPOINT:
        return paths.checkpoints
    if resource_type is ResourceType.LORA:
        return paths.loras
    if resource_type is ResourceType.EMBEDDING:
        return paths.embeddings
    raise DownloadError(f"Unsupported resource type: {resource_type}")


def _resolve_filename(path: str, content_disposition: Optional[str]) -> str:
    """Determine the filename from the URL path or ``Content-Disposition`` header."""

    name = Path(unquote(path)).name
    if name:
        return name

    if content_disposition:
        match = re.search(r"filename\*=UTF-8''(?P<fname>[^;]+)", content_disposition)
        if match:
            return unquote(match.group("fname"))
        match = re.search(r'filename="?([^";]+)"?', content_disposition)
        if match:
            return match.group(1)

    raise DownloadError("Unable to determine filename from response.")


def _infer_resource_type(path: str, filename: str) -> ResourceType:
    """Infer the resource type from the URL path and filename."""

    components = [segment.lower() for segment in Path(path).parts]
    name = filename.lower()
    suffix = Path(name).suffix

    if any("embedding" in segment for segment in components) or suffix in {".pt", ".bin"}:
        return ResourceType.EMBEDDING

    if any("lora" in segment for segment in components) or "lora" in name or suffix == ".zip":
        return ResourceType.LORA

    if suffix in {".safetensors", ".ckpt"}:
        return ResourceType.CHECKPOINT

    # Default to checkpoint if nothing else matches.
    return ResourceType.CHECKPOINT
