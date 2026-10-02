"""`stores update` must recompute a `content_hash` it has no reason to trust.

A shard written before per-field hashes existed carries a `content_hash` nothing verified, and
`migrate_hash_names` renames that key without recomputing it. Skipping re-extraction whenever
`source_hash` matched (the Markdown untouched in git) left the hash stale forever: `stores
check` kept reporting `data_mutation` for a file nobody had edited, and the reported workaround
was to delete the hash by hand and reindex.
"""

from __future__ import annotations

import json
from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.store import documents_hash
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.io.utils import yaml_dump, yaml_load
from sldb.store.layout import documents_shard_path

from tests.store.test_documents_shards import _Args, _store


def _shard(store: Path, root: Path, name: str) -> Path:
    m_entry = next(m for m in load_store_index(store).models if m.name == "Note")
    m_idx = load_models_index(root / m_entry.models_index)
    return documents_shard_path(store, "Note", name)


def _doc_names(store: Path, root: Path) -> list[str]:
    m_entry = next(m for m in load_store_index(store).models if m.name == "Note")
    m_idx = load_models_index(root / m_entry.models_index)
    return [d.name for d in load_documents_index(root / m_idx.documents_index).documents]


def _strip_field_hashes(path: Path) -> str:
    """The shard as a store written before per-field hashes existed: map empty, hash kept."""
    data = yaml_load(path.read_text(encoding="utf-8"))
    original = data["content_hash"]
    data.pop("field_hashes", None)
    path.write_text(yaml_dump(data), encoding="utf-8")
    return original


def _reopen(store: Path) -> None:
    """Drop the in-process shard cache, as a fresh process (a real edit's observer) would."""
    documents_hash.invalidate(store, "Note")


def test_update_recomputes_a_content_hash_it_cannot_trust(tmp_path: Path):
    store, root = _store(tmp_path, 1)
    name = _doc_names(store, root)[0]
    shard = _shard(store, root, name)
    original = _strip_field_hashes(shard)
    shard.write_text(shard.read_text(encoding="utf-8").replace(original, "d" * 64), encoding="utf-8")
    _reopen(store)

    update_store(_Args(store, root))

    reloaded = yaml_load(shard.read_text(encoding="utf-8"))
    assert reloaded["content_hash"] == original
    assert reloaded["field_hashes"]
    assert cli_main(["stores", "check", "--store", str(store), "--pythonpath", str(root)]) == 0


def test_update_backfills_field_hashes_of_an_older_shard(tmp_path: Path):
    store, root = _store(tmp_path, 1)
    shard = _shard(store, root, _doc_names(store, root)[0])
    original = _strip_field_hashes(shard)
    _reopen(store)

    update_store(_Args(store, root))

    reloaded = yaml_load(shard.read_text(encoding="utf-8"))
    assert reloaded["content_hash"] == original
    assert reloaded["field_hashes"]


def test_update_leaves_an_already_current_shard_untouched(tmp_path: Path):
    store, root = _store(tmp_path, 1)
    shard = _shard(store, root, _doc_names(store, root)[0])
    before = shard.read_text(encoding="utf-8")

    update_store(_Args(store, root))
    update_store(_Args(store, root))

    assert shard.read_text(encoding="utf-8") == before
