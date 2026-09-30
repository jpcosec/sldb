"""Turn nested spans into the full segment sequence, gaps included.

Nesting (see :mod:`sldb.core.segments.span_nesting`) only places the recorded
spans relative to each other; the characters no span claims are template text.
This module walks the nesting and emits a ``literal`` segment for every such gap,
so a consumer can concatenate a document's segments back into its exact text.
"""

from __future__ import annotations

from typing import Any

from sldb.core.segments.span_nesting import nest_nodes


def build_segment_tree(nodes: list[dict[str, Any]], text: str) -> list[dict[str, Any]]:
    """The full segment sequence for ``text``: nested nodes with literals between them.

    Args:
        nodes: Flat segment dicts carrying ``start``, ``end`` and ``_order``.
        text: The canonical text the offsets address.

    Returns:
        Top-level segments in reading order, each with a filled ``children`` list.
    """
    return interleave_literals(nest_nodes(nodes), text, 0, len(text))


def interleave_literals(nodes: list[dict[str, Any]], text: str, lo: int, hi: int) -> list[dict[str, Any]]:
    """Insert literal segments for the text not covered by ``nodes``.

    Args:
        nodes: Sibling segments, in reading order, inside ``[lo, hi)``.
        text: The canonical text the offsets address.
        lo: Start of the range being filled.
        hi: End of the range being filled.

    Returns:
        The siblings with literal segments inserted before, between and after them.
    """
    out: list[dict[str, Any]] = []
    cursor = lo
    for node in nodes:
        if node["start"] > cursor:
            out.append(literal(text, cursor, node["start"]))
        out.append(_fill_node(node, text))
        cursor = max(cursor, node["end"])
    if cursor < hi:
        out.append(literal(text, cursor, hi))
    return out


def _fill_node(node: dict[str, Any], text: str) -> dict[str, Any]:
    """Drop the ordering key of ``node`` and fill its children with literals.

    Args:
        node: A nested segment dict carrying ``start``, ``end`` and ``children``.
        text: The canonical text the offsets address.

    Returns:
        The same node, mutated, with a complete ``children`` sequence.
    """
    node.pop("_order", None)
    kids = node["children"]
    node["children"] = interleave_literals(kids, text, node["start"], node["end"]) if kids else []
    return node


def literal(text: str, start: int, end: int) -> dict[str, Any]:
    """A literal segment over ``text[start:end]``.

    Args:
        text: The canonical text.
        start: Inclusive start offset.
        end: Exclusive end offset.

    Returns:
        A ``literal`` segment dict.
    """
    return {"type": "literal", "start": start, "end": end, "text": text[start:end]}
