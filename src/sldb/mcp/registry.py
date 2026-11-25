"""Which tools each level serves."""

from __future__ import annotations

from mcp.types import ToolAnnotations

from sldb.mcp.read import ReadTools
from sldb.mcp.signal_server import SignalServer
from sldb.mcp.signals import SignalTools
from sldb.mcp.write import WriteTools

READ_ONLY = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)
PROPOSES = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=False, open_world_hint=False)
WRITES = ToolAnnotations(read_only_hint=False, destructive_hint=True, idempotent_hint=False, open_world_hint=False)

READ_TOOLS = ("list_models", "describe_model", "list_relation_types", "describe_relation_type", "read_document", "select_documents", "neighbors", "neighborhood", "list_views", "resolve_view", "anchors_resolve", "check_integrity")


def register_read(server: SignalServer, tools: ReadTools, signals: SignalTools) -> None:
    """The read tools (level 0, all read-only and idempotent) and `list_signals`."""
    for name in READ_TOOLS:
        server.add_tool(getattr(tools, name), annotations=READ_ONLY)
    server.add_tool(signals.list_signals, annotations=READ_ONLY)


def register_write(server: SignalServer, writes: WriteTools) -> None:
    """The write tools. A call above the server's level is refused before anything is read."""
    server.add_tool(writes.propose_changes, annotations=PROPOSES)
    server.add_tool(writes.apply_changes, annotations=WRITES)
    server.add_tool(writes.undo.undo_changes, annotations=WRITES)
