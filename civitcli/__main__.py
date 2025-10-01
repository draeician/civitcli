"""Module executed when running ``python -m civitcli``."""

from __future__ import annotations

from .cli import main

__all__ = ["main"]

if __name__ == "__main__":
    raise SystemExit(main())
