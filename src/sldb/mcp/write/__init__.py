"""The write operations of the MCP server: propose, then apply, through `sldb.api`.

`propose_changes` turns typed changes into a batch in the form of `sldb.api.apply_batch` with
the `expected_source_hash` guard of every document it touches and writes nothing. `apply_changes`
hands that same batch to `apply_batch`, which prevalidates it and applies it whole or not at
all. Nothing here validates, renders, serializes, keeps an index or touches a file: every check
is SLDB's. What SLDB does not offer yet is listed in `pending.PENDING` and every answer says so."""

from sldb.mcp.write.tools import DEFAULT_ACTOR, WriteTools

__all__ = ["DEFAULT_ACTOR", "WriteTools"]
