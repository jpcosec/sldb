"""Load and save a document index's derived file, keyed by its embedder."""

from __future__ import annotations

import json
from pathlib import Path


def read_index(path: Path, embedder_id: str) -> dict[str, dict]:
    """The entries of a derived index file, only when written by this same embedder."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if data.get("embedder") == embedder_id:
        return data.get("entries", {}) or {}
    return {}


def write_index(path: Path, embedder_id: str, entries: dict[str, dict]) -> None:
    """Write the derived index file: the embedder id and the entries."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"embedder": embedder_id, "entries": entries}), encoding="utf-8"
    )
