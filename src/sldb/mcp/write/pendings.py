"""Which pending items of SLDB an answer must declare."""

from __future__ import annotations

from sldb.mcp.mutability import CONTENT
from sldb.mcp.write.pending import PENDING


def level_pending(level: int) -> list[dict[str, str]]:
    """The missing store-hash precondition, when the batch writes rules."""
    return [PENDING["store_hash_precondition"]] if level > CONTENT else []
