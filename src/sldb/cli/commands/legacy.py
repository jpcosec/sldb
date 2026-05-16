from __future__ import annotations

from typing import Any

from sldb.cli.commands.links import LinkCLI
from sldb.cli.commands.query import QueryCLI


class LegacyCLI:
    """Compatibility surface for the raw pre-redesign commands."""

    def __init__(self) -> None:
        self._query = QueryCLI()
        self._links = LinkCLI()

    def run(self, args: Any) -> int:
        command = args.legacy_command
        if command in {"ls", "get", "glob", "find"}:
            return getattr(self._query, command)(args)
        if command in {"recover", "compose"}:
            return getattr(self._links, command)(args)
        raise SystemExit(f"Unknown legacy command: {command}")
