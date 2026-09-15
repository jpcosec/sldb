from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_sections_index,
    load_semantic_dag,
    load_store_index,
    save_documents_index,
    save_models_index,
    save_sections_index,
    save_semantic_dag,
    save_semantic_index,
)
from sldb.store.layout import sections_index_relpath
from sldb.store.models import (
    DocSections,
    SectionContextRecord,
    SectionsIndex,
    SemanticDAG,
    SemanticDocumentRecord,
    SemanticIndex,
    SemanticNode,
)
from sldb.store.semantic_doc_contribution import doc_contribution as _doc_contribution
from sldb.store.semantic_tags import _prefix_edges
import re
def _slugify(text: str) -> str: return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

logger = logging.getLogger(__name__)


@dataclass
class RebuildReport:
    docs_processed: int = 0
    docs_skipped_missing: int = 0
    docs_empty_sections: int = 0
    headings_no_map: int = 0
    verbose: list[str] = field(default_factory=list)


def _walk_model(m_entry, m_idx, root, resolver, py_path, report, stale: dict | None = None) -> dict:
    """The model's contribution to the semantic indexes: a document whose `hash_c` matches
    what `stale` (the model's last cached contribution, key or no key) recorded it as comes
    back unprocessed — extracted (and tagged) only when its text moved (PLAN 15 M2)."""
    d_idx = load_documents_index(root / m_idx.documents_index)
    stale_docs = (stale or {}).get("docs", {})
    docs, tags, prefix = {}, defaultdict(list), set()
    for doc in d_idx.documents:
        if not (d_path := root / doc.path).exists():
            report.docs_skipped_missing += 1; continue
        docs[doc.name] = _doc_contribution(doc, d_path, stale_docs.get(doc.name), m_entry, resolver, py_path, report)
        _note_tags(doc, tags, prefix)
    save_documents_index(root / m_idx.documents_index, d_idx)
    return {"docs": docs, "tags": dict(tags), "prefix": sorted(prefix)}


def _note_tags(doc, tags, prefix) -> None:
    for tag in doc.semantic_tags:
        tags[tag].append(doc.name); prefix.update(_prefix_edges(tag))


def _model_contribution(s_path, m_entry, root, resolver, py_path, report) -> dict:
    """From the built cache when the model's hash_b did not move; otherwise walked, reusing
    (from the same cache, key mismatch and all) the per-document work of every document
    whose own hash_c is unchanged — only a new or edited document is actually extracted."""
    from sldb.store import built_cache
    m_idx = load_models_index(root / m_entry.models_index)
    key = built_cache.model_key(m_idx)
    hit = built_cache.get(s_path, "semantic", m_entry.name, key)
    if hit is not None:
        report.docs_processed += len(hit["docs"]); return hit
    stale = built_cache.get_stale(s_path, "semantic", m_entry.name)
    value = _walk_model(m_entry, m_idx, root, resolver, py_path, report, stale=stale)
    built_cache.put(s_path, "semantic", m_entry.name, key, value)
    return value


def _merge(c: dict, docs_dict, t_to_d, p_by_n) -> None:
    for name, rec in c["docs"].items(): docs_dict[name] = SemanticDocumentRecord(model=rec["model"], path=rec["path"], tags=rec["tags"])
    for tag, names in c["tags"].items(): t_to_d[tag].extend(names)
    for p, child in c["prefix"]: p_by_n[child].add(p); p_by_n.setdefault(p, set())


def rebuild_semantic_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None = None, report: RebuildReport | None = None) -> RebuildReport:
    report = report or RebuildReport()
    d_dict, t_to_d, p_by_n, existing = {}, defaultdict(list), defaultdict(set), load_semantic_dag(store_path)
    for m in load_store_index(store_path).models: _merge(_model_contribution(store_path, m, project_root, resolve_model_ref, pythonpath, report), d_dict, t_to_d, p_by_n)
    for c, parents in existing.equivalences.items():
        p_by_n.setdefault(c, set())
        for p in parents: p_by_n[c].add(p); p_by_n.setdefault(p, set())
    _save_indexes(store_path, p_by_n, existing.equivalences, t_to_d, d_dict)
    return report


def _save_indexes(s_path, p_by_n, equiv, t_to_d, docs):
    nodes = [SemanticNode(id=n_id, parents=sorted(p)) for n_id, p in sorted(p_by_n.items())]
    save_semantic_dag(s_path, SemanticDAG(nodes=nodes, equivalences=equiv))
    tags = {t: sorted(d) for t, d in sorted(t_to_d.items())}
    save_semantic_index(s_path, SemanticIndex(tags=tags, documents=docs))


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
