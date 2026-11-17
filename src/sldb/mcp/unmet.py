"""A call that names a tool or an argument the server does not have: answered, not failed."""

from __future__ import annotations

from typing import Any

from sldb.mcp.context import ServerContext
from sldb.mcp.mutability import LEVELS
from sldb.mcp.signals import PENDING_TOOLS, settle
from sldb.mcp.signals.catalog import NOT_IMPLEMENTED, UNKNOWN_ARGUMENT, UNKNOWN_TOOL

#: The least write level that serves each write tool.
LEVEL_TOOLS = {"propose_changes": 1, "apply_changes": 1, "undo_changes": 1}


def why_missing(context: ServerContext, name: str) -> str:
    """Why this server has no tool `name`."""
    if name in PENDING_TOOLS:
        return f"{name} is not implemented yet: it {PENDING_TOOLS[name]}."
    if name in LEVEL_TOOLS:
        return f"{name} needs write level {LEVEL_TOOLS[name]}; this server was started with level {context.level} ({LEVELS[context.level]}). The level is set by the operator (`--level`), not by a tool argument."
    return f"this server has no tool {name!r}; list_tools names the ones it serves."


def unknown_tool(context: ServerContext, name: str, arguments: dict[str, Any], tools: list[str]) -> dict[str, Any]:
    """The answer to a call of a tool this server does not serve."""
    signal_class = NOT_IMPLEMENTED if name in PENDING_TOOLS else UNKNOWN_TOOL
    answer = {"signal": {"class": signal_class, "name": name, "candidates": tools}, "found": False, "tool": name, "explanation": why_missing(context, name)}
    return settle(context.log, context.store_path, name, arguments, answer)


def unknown_arguments(context: ServerContext, name: str, arguments: dict[str, Any], accepted: list[str]) -> dict[str, Any] | None:
    """The answer to a call that passes arguments the tool does not take, or None."""
    extra = [key for key in arguments if key not in accepted]
    if not extra:
        return None
    mark = {"class": UNKNOWN_ARGUMENT, "name": extra[0], "candidates": accepted}
    answer = {"signal": mark, "found": False, "tool": name, "unknown_arguments": extra, "explanation": f"{name} takes {accepted}, not {extra}; nothing was run."}
    return settle(context.log, context.store_path, name, arguments, answer)
