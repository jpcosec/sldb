"""Near names for a name that does not exist: `sldb.api.matching`, not a matcher of our own."""

from __future__ import annotations

from typing import Sequence

from sldb.api.matching import Matcher
from sldb.mcp.signals.catalog import SUGGESTIONS


def suggest(wanted: str, candidates: Sequence[str]) -> list[str]:
    """The first `SUGGESTIONS` candidates `Matcher.rank` ranks nearest to `wanted`, in its order."""
    ranked = Matcher().rank(wanted, [(name, name) for name in dict.fromkeys(candidates)], k=SUGGESTIONS)
    return [name for name, _ in ranked]
