"""`sldb stores migrate-hashes`: the letter keys become semantic names, values untouched."""

from __future__ import annotations

import yaml

from sldb.api import migrate_store_hash_names, store_fingerprint
from sldb.store.io import invalidate_index_cache, load_store_index
from sldb.store.io.shards import invalidate_shard_cache
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import core_dir

_LETTERS = {"store_hash": "hash_a", "model_hash": "hash_b", "source_hash": "hash_c", "content_hash": "hash_d"}


def _to_letters(value) -> None:
    if isinstance(value, dict):
        for new, old in _LETTERS.items():
            if new in value:
                value[old] = value.pop(new)
        for item in value.values():
            _to_letters(item)
    elif isinstance(value, list):
        for item in value:
            _to_letters(item)


def _make_legacy(store) -> None:
    for path in core_dir(store).rglob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        _to_letters(data)
        path.write_text(yaml_dump(data), encoding="utf-8")
    invalidate_index_cache()
    invalidate_shard_cache()


def test_migration_rewrites_keys_without_moving_hashes(api_store):
    _make_legacy(api_store.store)
    before = store_fingerprint(api_store.store)
    changed = migrate_store_hash_names(api_store.store)
    assert changed
    assert store_fingerprint(api_store.store) == before


def test_migration_writes_semantic_names(api_store):
    _make_legacy(api_store.store)
    migrate_store_hash_names(api_store.store)
    raw = yaml.safe_load((api_store.store / "core" / "store_index.yaml").read_text())
    assert "store_hash" in raw and "hash_a" not in raw
    assert load_store_index(api_store.store).store_hash
