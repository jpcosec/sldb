from __future__ import annotations
from typing import Any
from sldb.core.exceptions import SLDBError
from sldb.cli.commands.store_init import init_store
from sldb.cli.commands.store_add import add_store
from sldb.cli.commands.store_check import check_store
from sldb.cli.commands.store_migrate_hashes import migrate_hashes
from sldb.cli.commands.store_update import update_store
from sldb.cli.commands.store_semantic_map import semantic_map_store

class StoreCLI:
    """Handles store-level lifecycle and federation."""

    def _get_handler(self, cmd_name: str) -> Any:
        cmd_map = {
            "init": init_store,
            "add": add_store,
            "check": check_store,
            "migrate-hashes": migrate_hashes,
            "update": update_store,
            "semantic-map": semantic_map_store,
        }
        return cmd_map.get(cmd_name)

    def run(self, args: Any) -> int:
        """Dispatch store subcommands."""
        handler = self._get_handler(args.store_command)
        if not handler:
            raise SLDBError(f"Unknown store command: {args.store_command}")
        return handler(args)
