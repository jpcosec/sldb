"""One document's edges shard (the sections pattern, PLAN 15 capa 5): the shard, keyed by
`hash_c`, is the cache — a document whose `hash_c` matches what its shard already says is not
processed; a new or changed one is rebuilt and its shard (re)written, on its own, no other
document's shard is read or rewritten."""

from __future__ import annotations

from typing import Callable

from sldb.store.edge_index.cache_keys import edge_shard_version
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.io.shards import load_edges_shard, save_edges_shard
from sldb.store.layout import edges_shard_path
from sldb.store.models import DocEdges, DocumentEntry


def sync_doc_shard(store_path, doc: DocumentEntry, m_entry, report: EdgeRebuildReport, build_doc_edges: Callable[[DocumentEntry], DocEdges]) -> DocEdges:
    """This document's edges shard, current: reused untouched when it was built from this
    `hash_c` (and these tags, under these rules), rebuilt and rewritten otherwise.
    `build_doc_edges` is edge_rebuild's own builder, passed in rather than imported back."""
    path = edges_shard_path(store_path, m_entry.name, doc.name)
    cached = load_edges_shard(path, DocEdges)
    if cached is not None and _is_current(cached, doc):
        report.docs_reused += 1
        return cached
    fresh = build_doc_edges(doc).model_copy(update={"hash_c": doc.hash_c, "hash_d": doc.hash_d, "edges_version": edge_shard_version()})
    save_edges_shard(path, fresh)
    report.docs_written += 1
    return fresh


def _is_current(cached: DocEdges, doc: DocumentEntry) -> bool:
    """`hash_d` and the tags are compared too: both also depend on the model (its contract, its
    semantics), which can move without the document's text (and so its `hash_c`) moving."""
    same_hashes = (cached.hash_c, cached.hash_d) == (doc.hash_c, doc.hash_d)
    same_tags = cached.semantic_tags == sorted(set(doc.semantic_tags))
    return same_hashes and same_tags and cached.edges_version == edge_shard_version()
