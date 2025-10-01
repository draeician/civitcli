"""Command-line interface for :mod:`civitcli`."""

from __future__ import annotations

import argparse
import logging
from typing import Optional, Sequence

from . import __version__
from .downloader import DownloadError, download_resource

_LOG_FORMAT = "%(levelname)s: %(message)s"


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser used by the CLI."""

    parser = argparse.ArgumentParser(
        prog="civitcli",
        description="Tools for downloading Civitai resources and rendering stable-diffusion.cpp commands.",
    )
    parser.add_argument(
        "--download",
        metavar="URL",
        help="Download a resource from the provided Civitai URL.",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="Parse generation metadata and output a stable-diffusion.cpp command (future milestone).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity (can be supplied multiple times).",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def _configure_logging(verbosity: int) -> None:
    """Initialise logging according to the requested verbosity level."""

    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, format=_LOG_FORMAT)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for the console script."""

    parser = create_parser()
    args = parser.parse_args(argv)

    _configure_logging(args.verbose)

    exit_code = 0

    if args.download:
        try:
            result = download_resource(args.download)
        except DownloadError as exc:
            logging.error("Download failed: %s", exc)
            exit_code = 1
        else:
            logging.info("Downloaded %s to %s", result.filename, result.path)
    if args.render:
        logging.warning("Render functionality is not yet implemented in this milestone.")

    return exit_code


if __name__ == "__main__":  # pragma: no cover - handled by __main__.py
    raise SystemExit(main())
