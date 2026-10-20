"""Who is writing, for the `by` of every document's provenance block.

Resolved once per process: what the CLI's global `--actor` set, else `SLDB_ACTOR`, else the
bare `agent` (docs/architecture/provenance.md §1). An API caller passing `actor=` wins.
"""

from __future__ import annotations

import os

DEFAULT_ACTOR = "agent"
_SET: list[str] = []


def set_actor(actor: str | None) -> None:
    """Fix the actor for this process (the CLI's `--actor`); None clears it."""
    _SET.clear()
    if actor:
        _SET.append(actor)


def current_actor(explicit: str | None = None) -> str:
    """`explicit` when given, else the process actor, else `SLDB_ACTOR`, else `agent`."""
    return explicit or (_SET[0] if _SET else None) or os.environ.get("SLDB_ACTOR") or DEFAULT_ACTOR
