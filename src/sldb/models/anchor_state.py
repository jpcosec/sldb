"""The states of a code anchor and the class of each (docs/architecture/code-anchoring.md §4).

`ok`: the source is what the anchor saw. `alert`: the source moved against it (changed,
reconnected, lost, renormalize): valid, to be looked at, never silent. `error`: something is
broken (the file does not parse, the reference is malformed, tree-sitter is missing).
"""

from __future__ import annotations

from enum import Enum


class AnchorState(str, Enum):
    INTACT = "intact"
    CHANGED = "changed"
    RECONNECTED = "reconnected"
    LOST = "lost"
    RENORMALIZE = "renormalize"
    UNPARSEABLE = "unparseable"
    INVALID = "invalid"
    UNAVAILABLE = "unavailable"

    @property
    def level(self) -> str:
        """`ok`, `alert` or `error`: said once, here."""
        if self is AnchorState.INTACT:
            return "ok"
        return "error" if self in (AnchorState.UNPARSEABLE, AnchorState.INVALID, AnchorState.UNAVAILABLE) else "alert"
