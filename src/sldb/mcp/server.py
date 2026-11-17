"""The sldb MCP server over stdio: `sldb mcp --store <project>/.sldb --level 0|1|2 --actor <who>`.

Level 0 (the default) serves the read tools and `list_signals`, all read-only: none writes to
the store or to its linked stores. `--level 1` (content) adds `propose_changes`,
`apply_changes` and `undo_changes`; `--level 2` also lets them write the store's rules as data. The level is the
operator's, never a tool argument. A consumer adds tools of its own with `--extension
module:function` or `build_server(..., extensions=[...])`. Every tool returns structured JSON."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from sldb.mcp.context import ServerContext
from sldb.mcp.extension import Extension, load_extension
from sldb.mcp.mutability import READ
from sldb.mcp.read import ReadTools
from sldb.mcp.registry import register_read, register_write
from sldb.mcp.signal_server import SignalServer
from sldb.mcp.signals import SignalTools
from sldb.mcp.write import WriteTools

INSTRUCTIONS = (
    "Read-only access to one SLDB store and the stores it links. Documents are named "
    "`Model:name` (`alias:Model:name` in a linked store); every document carries its stable "
    "address `sldb://document/<export id>`. Sets come as pages {items, total, offset, limit, "
    "truncated, next_offset}; an empty set carries an `explanation`. Asking for what does not "
    "exist (a tool, model, document, field, relation type, view or argument) is not an error: "
    "it is registered as a signal, answered with near names, and listed by list_signals."
)
WRITE_INSTRUCTIONS = (
    " Writing is two steps: propose_changes (typed changes; writes nothing and answers what "
    "would be written) and apply_changes (the proposal exactly as returned; applied whole or "
    "not at all, or rejected with its cause). undo_changes undoes the last batches this session "
    "applied, guarded: a document someone else wrote since refuses it."
)


def build_server(store: str | Path, level: int = READ, actor: str | None = None, extensions: Sequence[Extension] = ()) -> SignalServer:
    """An MCP server whose tools read `store` through `sldb.api`, write it at `level` >= 1, and
    carry the tools and batch validators each of `extensions` (`extension(server, context)`)
    registers. Every extension runs here, before the server answers its first call."""
    context = ServerContext(store, level, actor)
    server = SignalServer(context, instructions=INSTRUCTIONS + (WRITE_INSTRUCTIONS if level > READ else ""))
    register_read(server, ReadTools(store), SignalTools(context.log))
    if level > READ:
        register_write(server, WriteTools(store, level, actor, context=context))
    for extension in extensions:
        extension(server, context)
    return server


def serve(store: str | Path, level: int = READ, actor: str | None = None, extensions: Sequence[str] = ()) -> None:
    """Serve `store` over stdio until the client goes away; `extensions` are `module:function`."""
    build_server(store, level, actor, [load_extension(spec) for spec in extensions]).run("stdio")
