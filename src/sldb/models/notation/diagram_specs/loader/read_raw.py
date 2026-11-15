"""`read_raw`: el YAML de un spec, sin validar."""

from __future__ import annotations

from pathlib import Path

import yaml

from sldb.notations.exceptions import ParseError


def read_raw(path: Path) -> dict:
    if not path.exists():
        raise ParseError(f"File not found: {path}")
    try:
        return yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        raise ParseError(f"YAML parse error in {path}: {exc}") from exc
