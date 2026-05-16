from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class RuntimeDocument:
    """
    In-memory representation of a tracked document and its payload.
    """

    store_name: str
    store_path: Path
    model_name: str
    model_type: type
    name: str
    path: str
    payload: dict[str, Any]
    semantic_tags: list[str]
