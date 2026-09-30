"""Nest the recorder's flat spans into a containment tree.

Spans come out of the recorder in wrap order, not in reading order, and a span
may sit inside another. Sorting by start, then widest first, then **latest wrap
first at an identical range**, lets one stack pass rebuild the nesting. That last
tiebreak is not cosmetic: a composition of a single piece covers exactly the same
characters as the ``render`` field that holds it, and without the rule the piece
would end up outside its own field.
"""

from __future__ import annotations

from typing import Any


def nest_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Nest overlapping segments by containment.

    Args:
        nodes: Flat segment dicts carrying ``start``, ``end`` and ``_order``.

    Returns:
        The root segments, with contained segments moved into ``children``.
    """
    ordered = sorted(nodes, key=lambda n: (n["start"], -n["end"], -n["_order"]))
    roots: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    for node in ordered:
        while stack and not contains(stack[-1], node):
            stack.pop()
        (stack[-1]["children"] if stack else roots).append(node)
        stack.append(node)
    return roots


def contains(outer: dict[str, Any], inner: dict[str, Any]) -> bool:
    """Whether ``outer`` spans over ``inner``.

    Args:
        outer: The candidate containing segment.
        inner: The candidate contained segment.

    Returns:
        True when inner's range fits inside outer's range.
    """
    return outer["start"] <= inner["start"] and inner["end"] <= outer["end"]
