"""The real package version, for provenance stamps such as `producer.version`."""

from __future__ import annotations

import re
import subprocess
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


def _source_checkout_dir() -> Path | None:
    """Directory of the pyproject.toml `_source_checkout_version` reads, same walk."""
    for parent in Path(__file__).resolve().parents[:5]:
        pyproject = parent / "pyproject.toml"
        if pyproject.is_file() and f'name = "{_DIST_NAME}"' in pyproject.read_text(encoding="utf-8"):
            return parent
    return None


def _git_describe(directory: Path) -> str | None:
    """`git -C <directory> describe --tags --always --dirty`, or None if git fails or is missing."""
    try:
        done = subprocess.run(
            ["git", "-C", str(directory), "describe", "--tags", "--always", "--dirty"],
            capture_output=True, text=True, timeout=2, check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    described = done.stdout.strip()
    return described if done.returncode == 0 and described else None


def source_revision() -> str | None:
    """`git describe --tags --always --dirty` of the source checkout, or None outside git."""
    checkout = _source_checkout_dir()
    if checkout is None or not (checkout / ".git").exists():
        return None
    return _git_describe(checkout)


def version_line() -> str:
    """`sldb <version> (<describe> at <checkout>)`, or `sldb <version>` outside a git checkout."""
    line = f"sldb {package_version()}"
    revision = source_revision()
    return f"{line} ({revision} at {_source_checkout_dir()})" if revision else line


def package_version() -> str:
    """Real package version: the source checkout's pyproject, else installed metadata."""
    checkout = _source_checkout_version()
    if checkout:
        return checkout
    try:
        return version(_DIST_NAME)
    except PackageNotFoundError:
        return "unknown"
