"""One document's semantic shard (PLAN 15 capa 5): the shard itself, keyed by `hash_c`, is
now the cache — a document whose `hash_c` matches what its shard already says is left
untouched; a new or changed one is extracted and its shard (re)written, on its own, no other
document's shard is read or rewritten."""

from __future__ import annotations

from sldb.store.codec import StoreCodec, default_codec
from sldb.store.io.shards import load_semantic_shard, save_semantic_shard
from sldb.store.layout import semantic_shard_path
from sldb.store.models import SemanticDocumentRecord
from sldb.store.semantic_doc_tags import tags_of as _tags_of


def process_doc(doc, doc_path, model_type, m_name, report, codec: StoreCodec = default_codec) -> SemanticDocumentRecord:
    report.docs_processed += 1
    doc.semantic_tags = list(_tags_of(doc, doc_path, model_type, m_name, codec))
    return SemanticDocumentRecord(model=m_name, path=doc.path, tags=doc.semantic_tags, hash_c=doc.hash_c)


def sync_doc_shard(store_path, doc, d_path, m_entry, resolver, py_path, report) -> SemanticDocumentRecord:
    """This document's semantic shard, current: reused untouched when its `hash_c` already
    matches what the shard on disk carries, (re)extracted and (re)written otherwise."""
    path = semantic_shard_path(store_path, m_entry.name, doc.name)
    cached = load_semantic_shard(path)
    if cached is not None and cached.hash_c == doc.hash_c:
        doc.semantic_tags = list(cached.tags)
        return cached
    rec = process_doc(doc, d_path, resolver(m_entry.model_ref, py_path), m_entry.name, report)
    save_semantic_shard(path, rec)
    return rec
