"""One-time rename of the persisted hash keys to their semantic names (spec 14 C10/D6).

The models read both namings (the validation aliases) and write only the new ones, so a
store migrates on its next save. This rewrites every YAML under `.sldb/core/` in place
instead, so a KB can commit the rename once, as its own change, without waiting for a write
and without touching any document's Markdown or its hash values.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load

_RENAMES = {"hash_a": "store_hash", "hash_b": "model_hash", "hash_c": "source_hash", "hash_d": "content_hash"}


def migrate_hash_names(store_path: Path) -> list[Path]:
    """Rewrite every `.sldb/core/**.yaml` still carrying a letter key; return the changed files."""
    from sldb.store.layout import core_dir

    return [path for path in sorted(core_dir(store_path).rglob("*.yaml")) if _migrate_file(path)]


def _migrate_file(path: Path) -> bool:
    data = yaml_load(path.read_text(encoding="utf-8"))
    if not _rename_keys(data):
        return False
    StoreIOUtils._atomic_write(path, yaml_dump(data))
    return True


def _rename_keys(value: Any) -> bool:
    if isinstance(value, dict):
        return _rename_mapping(value)
    if isinstance(value, list):
        return any(_rename_keys(item) for item in value)
    return False


def _rename_mapping(mapping: dict) -> bool:
    changed = False
    for old, new in _RENAMES.items():
        if old in mapping and new not in mapping:
            mapping[new] = mapping.pop(old)
            changed = True
    for item in mapping.values():
        changed |= _rename_keys(item)
    return changed
