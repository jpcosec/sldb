"""A model's hash_b, kept without re-reading every document shard on every write (PLAN 15
capa 7), extended in capa 8 to also serve the composed entries themselves and to persist
across operations: the cache is keyed by the model's own hash_b (read cheaply from its small
models_index file, not from the shards), so a fresh operation that finds nothing moved reuses
it verbatim — never recomposing all shards just because a new Store/World/CLI command
started. `note`/`forget` update it in place as this operation's own writes touch shards; a
mismatch against the on-disk hash_b (a hand edit, or `stores update`'s own full rescan)
recomposes once. `entries_of` hands out copies — a caller mutating one of its own is not
mutating this cache's.

Dirty tracking per namespace (one consumer's catch-up must not erase what another still
needs) lives in `documents_dirty`, called from here so `note`/`forget` stay each caller's
only touch point: `dirty_names`/`clear_dirty` below just forward to it."""

from __future__ import annotations

from pathlib import Path

from sldb.store import documents_dirty
from sldb.store.hashing import hash_document_entries
from sldb.store.models import DocumentEntry

_ENTRIES: dict[tuple[str, str], tuple[str, dict[str, DocumentEntry], int]] = {}
_GEN: dict[str, int] = {}


def new_operation(s_path: Path | None = None) -> None:
    """Bumps this store's operation generation (or, with no store, drops everything): a cache
    entry from a prior generation is re-validated against the model's on-disk hash_b before
    its next use in this one — reused untouched if nothing moved it, recomposed otherwise."""
    if s_path is None:
        _ENTRIES.clear()
        _GEN.clear()
        documents_dirty.clear_all()
        return
    _GEN[str(s_path)] = _GEN.get(str(s_path), 0) + 1


def invalidate(s_path: Path, model_name: str) -> None:
    """Drop one model's cache and every namespace's dirty baseline outright: something moved
    hash_c/hash_d (or might have) outside `note`/`forget`, so both are rebuilt (and a full
    comparison, not a partial dirty set) the next time either is used."""
    _ENTRIES.pop((str(s_path), model_name), None)
    documents_dirty.invalidate(s_path, model_name)


def _on_disk_hash_b(s_path: Path, model_name: str) -> str | None:
    from sldb.store.io import load_models_index, load_store_index
    from sldb.store.layout import project_root

    entry = next((m for m in load_store_index(s_path).models if m.name == model_name), None)
    return None if entry is None else load_models_index(project_root(s_path) / entry.models_index).hash_b


def _compose(s_path: Path, model_name: str) -> dict[str, DocumentEntry]:
    from sldb.store.io.shard_compose import compose_documents_entries

    return {e.name: e for e in compose_documents_entries(s_path, model_name)}


def _hash_b(entries: dict[str, DocumentEntry]) -> str:
    return hash_document_entries((e.name, e.hash_c, e.hash_d) for e in entries.values())


def _get(s_path: Path, model_name: str) -> tuple[str, dict[str, DocumentEntry]]:
    key, gen = (str(s_path), model_name), _GEN.get(str(s_path), 0)
    cached = _ENTRIES.get(key)
    if cached is not None and (cached[2] == gen or cached[0] == _on_disk_hash_b(s_path, model_name)):
        _ENTRIES[key] = (cached[0], cached[1], gen)
        return cached[0], cached[1]
    entries = _compose(s_path, model_name)
    _ENTRIES[key] = (_hash_b(entries), entries, gen)
    return _ENTRIES[key][0], entries


def _restamp(s_path: Path, model_name: str, entries: dict[str, DocumentEntry]) -> None:
    _ENTRIES[(str(s_path), model_name)] = (_hash_b(entries), entries, _GEN.get(str(s_path), 0))


def note(s_path: Path, model_name: str, entry: DocumentEntry) -> None:
    """This document's shard was just written as `entry`."""
    _, entries = _get(s_path, model_name)
    entries[entry.name] = entry
    _restamp(s_path, model_name, entries)
    documents_dirty.mark(s_path, model_name, entry.name)


def forget(s_path: Path, model_name: str, doc_name: str) -> None:
    """This document's shard was just deleted."""
    _, entries = _get(s_path, model_name)
    entries.pop(doc_name, None)
    _restamp(s_path, model_name, entries)
    documents_dirty.mark(s_path, model_name, doc_name)


def hash_b_of(s_path: Path, model_name: str) -> str:
    return _get(s_path, model_name)[0]


def count_of(s_path: Path, model_name: str) -> int:
    return len(_get(s_path, model_name)[1])


def entries_of(s_path: Path, model_name: str) -> list[DocumentEntry]:
    return [e.model_copy() for e in _get(s_path, model_name)[1].values()]


def dirty_names(s_path: Path, model_name: str, namespace: str) -> set[str] | None:
    """Names noted/forgotten in `namespace` ("semantic", "sections", ...) since its last
    `clear_dirty` — or None with no baseline to trust: the caller's cue to compare every
    document once instead."""
    return documents_dirty.names(s_path, model_name, namespace)


def clear_dirty(s_path: Path, model_name: str, namespace: str) -> None:
    """This namespace's consumer just brought every one of this model's documents current."""
    documents_dirty.clear(s_path, model_name, namespace)
