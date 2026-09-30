"""Decide whether a field's surface owns its own block of the document.

The UI renders a block field as a standalone editable region and an inline field
inside a line of prose, so this is part of the contract rather than a styling
detail. A field is a block when it starts a line, ends a line, and is separated
from its neighbours by a blank line or by the document's own border.
"""

from __future__ import annotations


def display_of(text: str, start: int, end: int) -> str:
    """Whether ``text[start:end]`` is a block of its own or sits inline.

    Args:
        text: The canonical document text.
        start: Inclusive start offset of the field's surface.
        end: Exclusive end offset of the field's surface.

    Returns:
        ``"block"`` when the field occupies its own block, else ``"inline"``.
    """
    if not _on_own_lines(text, start, end):
        return "inline"
    return "block" if _blank_bounded(text, start, end) else "inline"


def _on_own_lines(text: str, start: int, end: int) -> bool:
    """Whether the span starts at a line start and ends at a line end.

    Args:
        text: The canonical document text.
        start: Inclusive start offset.
        end: Exclusive end offset.

    Returns:
        True when no other text shares the span's first and last lines.
    """
    starts_line = start == 0 or text[start - 1] == "\n"
    return starts_line and (end == len(text) or text[end] == "\n")


def _blank_bounded(text: str, start: int, end: int) -> bool:
    """Whether a blank line or a document border sits on both sides.

    Args:
        text: The canonical document text.
        start: Inclusive start offset.
        end: Exclusive end offset.

    Returns:
        True when the span is separated from its neighbours by blank lines.
    """
    before = start == 0 or text[max(0, start - 2):start] == "\n\n"
    return before and (end == len(text) or text[end:end + 2] == "\n\n")
