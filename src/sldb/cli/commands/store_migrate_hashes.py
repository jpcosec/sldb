"""`sldb stores migrate-hashes`: the CLI adapter over `sldb.api.migrate_store_hash_names`."""

from __future__ import annotations

from typing import Any

from sldb.api.stores.migrate_hash_names import migrate_store_hash_names
from sldb.cli.store_context import get_store_context


def migrate_hashes(args: Any) -> int:
    sp, _root = get_store_context(args.store)
    changed = migrate_store_hash_names(sp)
    print(f"Migrated {len(changed)} index file(s) under {sp}")
    return 0
