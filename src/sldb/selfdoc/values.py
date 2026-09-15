"""Deterministic formatting of argparse metadata."""
from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any


def qualified_name(value: Any) -> str:
    """Name a callable or type without memory-address-dependent repr output."""
    return f"{value.__module__}.{value.__qualname__}"


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if callable(value) and hasattr(value, "__qualname__"):
        return qualified_name(value)
    raise ValueError(f"Unsupported parser metadata type: {type(value).__name__}")


def json_value(value: Any) -> str:
    """Represent a parser default/choice deterministically or reject it."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False, default=_json_default)
