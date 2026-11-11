"""One document's edges shard (the sections pattern, PLAN 15 capa 5): the shard, keyed by
`source_hash`, is the cache — a document whose `source_hash` matches what its shard already says is not
processed; a new or changed one is rebuilt and its shard (re)written, on its own, no other
document's shard is read or rewritten."""

from __future__ import annotations

from typing import Callable

from sldb.store.edge_index.cache_keys import edge_shard_version
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.io.shards import load_edges_shard, save_edges_shard
from sldb.store.hashing import hash_text, read_source_text, source_stat, unreadable_reason
from sldb.store.layout import edges_shard_path, project_root
from sldb.store.models import DocEdges, DocumentEntry


def sync_doc_shard(store_path, doc: DocumentEntry, m_entry, report: EdgeRebuildReport, build_doc_edges: Callable[[DocumentEntry], DocEdges], contract: str = "", signature: str | None = None) -> DocEdges:
    """This document's edges shard, current: reused untouched when it was built from this
    `source_hash` (and these tags, under these rules, and this `contract_signature` of the
    model when one is given), rebuilt and rewritten otherwise.
    `build_doc_edges` is edge_rebuild's own builder, passed in rather than imported back."""
    path = edges_shard_path(store_path, m_entry.name, doc.name)
    cached = load_edges_shard(path, DocEdges)
    if cached is not None and _is_current(cached, doc, contract) and _same_signature(cached, m_entry.name, doc.name, signature):
        report.docs_reused += 1
        return _with_current_stat(path, cached, store_path, doc)
    stamp = {"source_hash": doc.source_hash, "content_hash": doc.content_hash, "contract_hash": contract, "edges_version": edge_shard_version(), "source_stat": built_stat(store_path, doc)}
    fresh = build_doc_edges(doc).model_copy(update=stamp)
    save_edges_shard(path, fresh)
    report.docs_written += 1
    return fresh


def _is_current(cached: DocEdges, doc: DocumentEntry, contract: str) -> bool:
    """`content_hash`, the tags and the model's contract are compared too: each can move without
    the document's text (and so its `source_hash`) moving."""
    same_hashes = (cached.source_hash, cached.content_hash) == (doc.source_hash, doc.content_hash)
    same_tags = cached.semantic_tags == sorted(set(doc.semantic_tags))
    return same_hashes and same_tags and cached.contract_hash == contract and cached.edges_version == edge_shard_version()


def _same_signature(cached: DocEdges, model: str, name: str, signature: str | None) -> bool:
    """The document node was built under the model's current fields and declared references
    (a new `__references__` entry moves no hash); a shard without that node is not compared."""
    node = next((n for n in cached.nodes if n.id == doc_node_id(f"{model}:{name}")), None)
    return signature is None or node is None or node.contract_signature == signature


def _with_current_stat(path, cached: DocEdges, store_path, doc: DocumentEntry) -> DocEdges:
    """A reused shard whose `source_stat` is missing (built before it existed) or no longer the
    file's gets it, so the next read of the index need not open the file; one whose file does
    not hash to its `source_hash` keeps what it has (the read then hashes it and calls it stale)."""
    root = project_root(store_path)
    if cached.source_stat is not None and list(cached.source_stat) == source_stat(root / doc.path):
        return cached
    current = built_stat(store_path, doc)
    if current is None or current == cached.source_stat:
        return cached
    updated = cached.model_copy(update={"source_stat": current})
    save_edges_shard(path, updated)
    return updated


def built_stat(store_path, doc: DocumentEntry) -> list[int] | None:
    """`[mtime_ns, size]` of the document's file when its text hashes to the entry's
    `source_hash` (stat, read, stat again, all equal); None when the file may not be read
    (`hashing.unreadable_reason`), is gone, or moved since it was tracked: an edit made outside sldb before
    this build must not be stamped as current."""
    root = project_root(store_path)
    file = root / doc.path
    if unreadable_reason(root, file) is not None or (before := source_stat(file)) is None:
        return None
    try:
        text = read_source_text(file)
    except (OSError, UnicodeDecodeError):
        return None
    return before if hash_text(text) == doc.source_hash and source_stat(file) == before else None
