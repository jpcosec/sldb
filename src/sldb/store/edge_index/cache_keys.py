"""What invalidates the edge index's caches, besides a document's own `source_hash`."""

from __future__ import annotations

from pathlib import Path

from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
from sldb.store.io import load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.models import ModelsIndex
from sldb.store.section_paths import SECTION_INDEX_VERSION


def edge_shard_version() -> str:
    """Stamp of the rules a shard was built under: the index's own and the sections' (a
    document's section nodes are read from its sections shard)."""
    return f"{EDGE_INDEX_VERSION}|sections:{SECTION_INDEX_VERSION}"


def edge_cache_key(m_idx: ModelsIndex) -> str:
    """A model whose key has not moved (documents, version, semantics, ref, rules) is not walked."""
    from sldb.store import built_cache

    return f"{built_cache.model_key(m_idx)}|{m_idx.model_ref}|edges:{edge_shard_version()}"


def roster_state(store_path: Path) -> list[list]:
    """Per model: its name and the roster hash of its models index. A document written in place
    (its text, not its place) moves that hash even when no directory's stat moved, so a cache
    keyed on this and on stats alone never keeps what a rewrite changed."""
    root = project_root(store_path)
    return [[m.name, _roster_hash(root / m.models_index)] for m in load_store_index(store_path).models]


def _roster_hash(models_index: Path) -> str | None:
    try:
        return load_models_index(models_index).roster_hash
    except (OSError, ValueError):
        return None
