"""What invalidates the edge index's caches, besides a document's own `hash_c`."""

from __future__ import annotations

from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
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
