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


def scan_heading_bodies(markdown: str) -> dict[str, list[str]]:
    """The raw text under each heading (up to the next heading), keyed by its `format_heading` line.

    Read from the same AST as `scan_headings`, so ATX, setext and indented headings all
    get their real body. A heading repeated in the document appends one body per occurrence.
    """
    lines = markdown.splitlines()
    heads = []
    for node in AST_Handler().split_nodes(markdown):
        pair = _heading_of(node)
        if pair is not None and node.map:
            heads.append((format_heading(*pair), node.map[0], node.map[1]))
    bodies: dict[str, list[str]] = {}
    for i, (key, _start, end) in enumerate(heads):
        stop = heads[i + 1][1] if i + 1 < len(heads) else len(lines)
        bodies.setdefault(key, []).append("\n".join(lines[end:stop]))
    return bodies


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
