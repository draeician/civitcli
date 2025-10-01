"""Smoke tests for the civitcli command-line interface."""

from __future__ import annotations

import subprocess
import sys


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
