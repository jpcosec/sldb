"""The real package version, for provenance stamps such as `producer.version`."""

from __future__ import annotations

import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

_DIST_NAME = "structuredLanguageDB"


def _source_checkout_version() -> str | None:
    """Version in the pyproject.toml above `src/`, when running from a source tree."""
    for parent in Path(__file__).resolve().parents[:5]:
        pyproject = parent / "pyproject.toml"
        if pyproject.is_file():
            text = pyproject.read_text(encoding="utf-8")
            if f'name = "{_DIST_NAME}"' in text:
                match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
                return match.group(1) if match else None
    return None


def package_version() -> str:
    """Real package version: the source checkout's pyproject, else installed metadata."""
    checkout = _source_checkout_version()
    if checkout:
        return checkout
    try:
        return version(_DIST_NAME)
    except PackageNotFoundError:
        return "unknown"
