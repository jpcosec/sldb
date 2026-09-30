"""Read the headings out of a Markdown string, as (level, title) pairs.

Lives in `sldb.api` rather than `sldb.cli.graph_ops` because structural-noise
detection is an API concern and nothing in `api` may import `cli`.
"""

from __future__ import annotations

import re

from sldb.core.ast import AST_Handler
from sldb.core.contracts import MARKER_PATTERN

_HEADING_TAG = re.compile(r"h[1-6]")


def scan_headings(markdown: str) -> list[tuple[int, str]]:
    """Every heading in `markdown`, in document order.

    Args:
        markdown: The Markdown source (a template or a rendered document).

    Returns:
        One `(level, title)` pair per heading; `level` is 1 for `#`, 2 for `##`.
    """
    nodes = AST_Handler().split_nodes(markdown)
    found = (_heading_of(node) for node in nodes)
    return [pair for pair in found if pair is not None]


def _heading_of(node) -> tuple[int, str] | None:
    """The `(level, title)` of a heading node, or None when it is not a heading."""
    if not _HEADING_TAG.fullmatch(node.tag or ""):
        return None
    title = (node.find_leaf_text() or node.content or "").strip()
    return (int(node.tag[1]), title) if title else None


def is_wildcard(title: str) -> bool:
    """Whether a template heading is a marker slot (`⸢rev•title⸥`) and not a literal."""
    return re.search(MARKER_PATTERN, title) is not None


def format_heading(level: int, title: str) -> str:
    """A heading rendered back to its Markdown line, for error messages."""
    return f"{'#' * level} {title}"
