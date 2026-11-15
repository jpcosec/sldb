"""The MCP server of sldb: every tool is guarded, and an unmet call is a signal, not an error."""

from __future__ import annotations

import json
from typing import Any, Callable

from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult, TextContent

from sldb.mcp.context import ServerContext
from sldb.mcp.guard import guarded
from sldb.mcp.unmet import unknown_arguments, unknown_tool


class SignalServer(MCPServer):
    """An `MCPServer` that wraps each tool it is given (the built-in ones and an extension's)
    with `guarded`, and answers a call to a tool it lacks, or with arguments the tool does not
    take, as a logged signal with suggestions."""

    def __init__(self, context: ServerContext, **options: Any) -> None:
        super().__init__("sldb", **options)
        self.context = context

    def add_tool(self, fn: Callable[..., Any], name: str | None = None, **options: Any) -> None:
        name = name or fn.__name__
        super().add_tool(guarded(self.context, name, fn), name=name, **options)

    async def call_tool(self, name: str, arguments: dict[str, Any], context: Any = None) -> Any:
        served = {tool.name: tool for tool in await self.list_tools()}
        if name not in served:
            return answered(unknown_tool(self.context, name, arguments, sorted(served)))
        accepted = list(served[name].input_schema.get("properties", {}))
        unmet = unknown_arguments(self.context, name, arguments, accepted)
        return answered(unmet) if unmet is not None else await super().call_tool(name, arguments, context)


def answered(answer: dict[str, Any]) -> CallToolResult:
    """A structured, non-error result carrying `answer`."""
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(answer, ensure_ascii=False))], structured_content=answer, is_error=False)
