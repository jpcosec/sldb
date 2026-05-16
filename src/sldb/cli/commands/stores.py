from __future__ import annotations

from typing import Any

from sldb.cli.commands.store import StoreCLI


class StoresCLI:
    """Plural store surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._store = StoreCLI()

    def run(self, args: Any) -> int:
        args.store_command = args.stores_command
        return self._store.run(args)
