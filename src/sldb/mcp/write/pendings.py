"""Which pending items of SLDB an answer must declare."""

from __future__ import annotations

from sldb.mcp.changes import EDGE_MODEL, BatchChange
from sldb.mcp.mutability import CONTENT
from sldb.mcp.write.pending import PENDING


def edge_pending(changes: list[BatchChange]) -> list[dict[str, str]]:
    """The missing edge validation, when the batch creates an edge."""
    return [PENDING["edge_validation_before_write"]] if any(c.model == EDGE_MODEL and c.action == "create" for c in changes) else []


def level_pending(level: int) -> list[dict[str, str]]:
    """The missing store-hash precondition, when the batch writes rules."""
    return [PENDING["store_hash_precondition"]] if level > CONTENT else []
