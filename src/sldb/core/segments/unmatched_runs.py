"""The stretches of raw markdown that no field and no template literal explains.

These are the runs the alignment reports as ``insert`` or ``replace`` on the raw
side: text that survived extraction without a home. They are trimmed of
surrounding whitespace and dropped when empty, because a blank run is a layout
difference, not unexplained content the consumer should be shown.
"""

from __future__ import annotations

from typing import Any

from sldb.core.segments.canonical_alignment import Opcode

UNMATCHED_TAGS = ("insert", "replace")


def unmatched_runs(opcodes: list[Opcode], raw: str) -> list[dict[str, Any]]:
    """Every run of ``raw`` the canonical render does not account for.

    Args:
        opcodes: The alignment from :func:`sldb.core.segments.canonical_alignment.align`.
        raw: The markdown the payload was extracted from.

    Returns:
        Trimmed ``{start, end, text}`` ranges, blank ones removed.
    """
    runs = [trimmed(raw, j1, j2) for tag, _, _, j1, j2 in opcodes if tag in UNMATCHED_TAGS]
    return [run for run in runs if run["text"]]


def trimmed(text: str, start: int, end: int) -> dict[str, Any]:
    """A range with its surrounding whitespace excluded from the offsets.

    Args:
        text: The text the offsets address.
        start: Inclusive start offset.
        end: Exclusive end offset.

    Returns:
        A ``{start, end, text}`` range tightened to the non-blank content.
    """
    chunk = text[start:end]
    start += len(chunk) - len(chunk.lstrip())
    end -= len(chunk) - len(chunk.rstrip())
    return {"start": start, "end": end, "text": text[start:end] if start < end else ""}
