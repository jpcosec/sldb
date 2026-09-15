from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from sldb.store import documents_hash
from sldb.store.io import (
    load_models_index,
    load_semantic_dag,
    load_store_index,
    save_semantic_dag,
)
from sldb.store.io.shards import prune_shards, save_document_shard
from sldb.store.layout import documents_shard_path, semantic_shards_dir
from sldb.store.semantic_dag_sync import sync_semantic_dag
from sldb.store.semantic_doc_contribution import sync_doc_shard


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@dataclass
class RebuildReport:
    docs_processed: int = 0
    docs_skipped_missing: int = 0
    docs_empty_sections: int = 0
    headings_no_map: int = 0
    verbose: list[str] = field(default_factory=list)


def _sync_model(store_path, m_entry, root, resolver, py_path, report, new_tags: set) -> None:
    """Every document's semantic shard brought current; skipped whole when the model's
    hash_b (covering every one of its documents) has not moved since the last sync — no
    shard is even opened (PLAN 15 capa 5)."""
    from sldb.store import built_cache

    m_idx = load_models_index(root / m_entry.models_index)
    key = built_cache.model_key(m_idx)
    if built_cache.get(store_path, "semantic_shards", m_entry.name, key) is not None:
        return
    _sync_model_docs(store_path, m_entry, m_idx, root, resolver, py_path, report, new_tags)
    built_cache.put(store_path, "semantic_shards", m_entry.name, key, True)


def _sync_model_docs(store_path, m_entry, m_idx, root, resolver, py_path, report, new_tags: set) -> None:
    """PLAN 15 capa 7: a document's own shard (name, path, hash_c, hash_d, semantic_tags) is
    rewritten only when its semantic_tags actually changed by this sync — not the whole
    model's documents index, and not every document's shard just because one changed. PLAN
    15 capa 8: with a trustworthy dirty set (this operation's own writes, or a prior sync's
    clean baseline), only those documents are even opened — an untouched one's semantic
    shard is never read just to confirm it agrees with a hash_c that has not moved."""
    entries = {e.name: e for e in documents_hash.entries_of(store_path, m_entry.name)}
    dirty = documents_hash.dirty_names(store_path, m_entry.name, "semantic")
    to_sync = entries.values() if dirty is None else (entries[n] for n in dirty if n in entries)
    for doc in to_sync:
        _sync_one(store_path, doc, m_entry, root, resolver, py_path, report, new_tags)
    prune_shards(semantic_shards_dir(store_path, m_entry.name), set(entries))
    documents_hash.clear_dirty(store_path, m_entry.name, "semantic")


def _sync_one(store_path, doc, m_entry, root, resolver, py_path, report, new_tags: set) -> None:
    if not (d_path := root / doc.path).exists():
        report.docs_skipped_missing += 1
        return
    before = list(doc.semantic_tags)
    rec = sync_doc_shard(store_path, doc, d_path, m_entry, resolver, py_path, report)
    new_tags.update(rec.tags)
    if doc.semantic_tags != before:
        save_document_shard(documents_shard_path(store_path, m_entry.name, doc.name), doc)
        documents_hash.note(store_path, m_entry.name, doc)


def rebuild_semantic_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None = None, report: RebuildReport | None = None) -> RebuildReport:
    report = report or RebuildReport()
    new_tags: set[str] = set()
    for m in load_store_index(store_path).models:
        _sync_model(store_path, m, project_root, resolve_model_ref, pythonpath, report, new_tags)
    sync_semantic_dag(store_path, new_tags)
    return report


def _about_terms(breadcrumbs: list[str], semantic_tags: list[str]) -> list[str]:
    seen, terms = set(), []
    for b in breadcrumbs:
        if (r := b.strip()) and r not in seen: seen.add(r); terms.append(r)
        if (n := _slugify(r).replace("-", " ").strip()) and n not in seen: seen.add(n); terms.append(n)
    for tag in semantic_tags:
        if tag not in seen: seen.add(tag); terms.append(tag)
    return terms


def add_semantic_equivalence(store_path: Path, local_tag: str, global_tag: str) -> None:
    """Adds a semantic equivalence mapping to the store DAG."""
    dag = load_semantic_dag(store_path)
    mapped = set(dag.equivalences.get(local_tag, []))
    mapped.add(global_tag)
    dag.equivalences[local_tag] = sorted(mapped)
    save_semantic_dag(store_path, dag)
