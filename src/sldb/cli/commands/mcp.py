"""CLI entry point of `sldb mcp`: serve a store over stdio, with `mcp` imported only here."""

from __future__ import annotations

import sys
from typing import Any

from sldb.api.actor import DEFAULT_ACTOR, current_actor

INSTALL = "sldb mcp needs the optional `mcp` extra: install it with `pip install 'structuredLanguageDB[mcp]'` (or `uv pip install 'mcp>=2.2'`)."


def process_actor(args: Any) -> str | None:
    """`--actor` (the CLI takes the global one off the arguments, into the process), or None."""
    actor = current_actor(getattr(args, "actor", None))
    return None if actor == DEFAULT_ACTOR else actor


class McpCLI:
    def run(self, args: Any) -> int:
        try:
            from sldb.mcp.server import serve
        except ModuleNotFoundError as error:
            if (error.name or "").split(".")[0] != "mcp":
                raise
            print(INSTALL, file=sys.stderr)
            return 2
        serve(args.store, args.level, process_actor(args), args.extension)
        return 0
