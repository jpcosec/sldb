"""Constants and ids of projection views."""

from __future__ import annotations

from pathlib import Path

VIEW_MODEL = "ViewDoc"
DIRECTIONS = ("both", "outgoing", "incoming")
DOCUMENT_PREFIX = "sldb://document/"
VIEWS_DIR = Path("sldb") / "views"


def node_id(model: str, name: str) -> str:
    """The edge-index id of a document: ``sldb://document/<Model>:<name>``."""
    return f"{DOCUMENT_PREFIX}{model}:{name}"
