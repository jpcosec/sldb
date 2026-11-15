"""Every tool goes through here: failures reach the agent with their cause, and what a tool
marked as a signal is logged and answered with suggestions."""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable

from mcp.server.mcpserver.exceptions import ToolError

from sldb.mcp.context import ServerContext
from sldb.mcp.signals import settle


def signature_of(tool: Callable[..., Any]) -> inspect.Signature:
    """The signature of `tool` with its annotations resolved, so the wrapper keeps them."""
    try:
        return inspect.signature(tool, eval_str=True)
    except (NameError, TypeError):
        return inspect.signature(tool)


def guarded(context: ServerContext, name: str, tool: Callable[..., Any]) -> Callable[..., Any]:
    """`tool` with any failure (a bad argument, a predicate SLDB cannot parse, a view SLDB
    cannot resolve) answered as a tool error that names its cause, and its answer settled."""

    @functools.wraps(tool)
    def run(**arguments: Any) -> Any:
        try:
            answer = tool(**arguments)
        except Exception as error:  # every failure reaches the agent with its cause
            raise ToolError(f"{type(error).__name__}: {error}") from error
        return settle(context.log, context.store_path, name, arguments, answer) if isinstance(answer, dict) else answer

    run.__signature__ = signature_of(tool)  # type: ignore[attr-defined]
    return run
