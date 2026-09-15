"""One document's sections shard (PLAN 15 capa 5): the shard, keyed by `hash_c`, is the
cache — a document whose `hash_c` matches what its shard already says is left unparsed; a
new or changed one is parsed and its shard (re)written, on its own, no other document's
shard is read or rewritten."""

from __future__ import annotations

from sldb.store.io.shards import load_sections_shard, save_sections_shard
from sldb.store.layout import sections_shard_path
from sldb.store.models import DocSections
from sldb.store.section_paths import SECTION_INDEX_VERSION


def sync_doc_shard(store_path, doc, d_path, m_entry, report, process_doc_sections) -> DocSections:
    """This document's sections shard, current: reused untouched when its `hash_c` already
    matches what the shard on disk carries, (re)parsed and (re)written otherwise.
    `process_doc_sections` is section_rebuild's own parser, passed in rather than imported
    back (this module is the one section_rebuild imports)."""
    path = sections_shard_path(store_path, m_entry.name, doc.name)
    cached = load_sections_shard(path)
    if cached is not None and cached.hash_c == doc.hash_c and cached.sections_version == SECTION_INDEX_VERSION:
        return _reused(cached, report)
    fresh = process_doc_sections(doc, d_path, report).model_copy(update={"hash_c": doc.hash_c, "sections_version": SECTION_INDEX_VERSION})
    save_sections_shard(path, fresh)
    return fresh


def _reused(cached: DocSections, report) -> DocSections:
    report.docs_processed += 1
    if not cached.sections:
        report.docs_empty_sections += 1
    return cached
