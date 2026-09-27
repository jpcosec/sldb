"""`sldb stores migrate-hashes`: rewrite the persisted letter keys as their semantic names.

Thin api wrapper over ``sldb.store.migration_hash_names`` so the CLI (and any consumer) names
only ``sldb.api``. Reads accept both namings; this is the explicit, one-commit migration.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.migration_hash_names import migrate_hash_names as _migrate_hash_names


def migrate_store_hash_names(store_path: Path) -> list[Path]:
    """Rename hash_a..hash_d to store/model/source/content across `.sldb/core/`; return changed files."""
    return _migrate_hash_names(store_path)
