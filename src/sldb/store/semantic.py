from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from sldb.store.codec import StoreCodec, default_codec
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
from sldb.store.semantic_tags import collect_document_semantic_tags, _prefix_edges
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


_DOC_TAGS: dict[tuple, list[str]] = {}   # (path, mtime, size, model) -> semantic tags; a rebuild only extracts what changed


def _file_signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


def _extract_tags(doc_path: Path, model_type, m_name: str, codec: StoreCodec) -> list[str]:
    from sldb.store.runtime_cache import payload_of
    payload = payload_of(doc_path, m_name) if codec is default_codec else None
    if payload is None:
        try: payload = codec.extract(model_type, doc_path.read_text(encoding="utf-8"))
        except Exception: payload = {}
    return collect_document_semantic_tags(model_type, payload)


def _tags_of(doc_path: Path, model_type, m_name: str, codec: StoreCodec) -> list[str]:
    key = (str(doc_path), *_file_signature(doc_path), m_name)
    tags = _DOC_TAGS.get(key) if codec is default_codec else None
    if tags is None:
        tags = _extract_tags(doc_path, model_type, m_name, codec)
        if codec is default_codec: _DOC_TAGS[key] = tags
    return tags


def _process_doc(doc, doc_path, model_type, m_name, report, codec: StoreCodec = default_codec):
    report.docs_processed += 1
    doc.semantic_tags = list(_tags_of(doc_path, model_type, m_name, codec))
    return SemanticDocumentRecord(model=m_name, path=doc.path, tags=doc.semantic_tags)


def _process_model_semantics(m_entry, root, resolver, py_path, report, docs_dict, t_to_d, p_by_n):
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    for doc in d_idx.documents:
        if not (d_path := root / doc.path).exists():
            report.docs_skipped_missing += 1; continue
        docs_dict[doc.name] = _process_doc(doc, d_path, resolver(m_entry.model_ref, py_path), m_entry.name, report)
        for tag in doc.semantic_tags:
            t_to_d[tag].append(doc.name)
            for p, c in _prefix_edges(tag): p_by_n[c].add(p); p_by_n.setdefault(p, set())
    save_documents_index(root / m_idx.documents_index, d_idx)

def rebuild_semantic_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None = None, report: RebuildReport | None = None) -> RebuildReport:
    report = report or RebuildReport()
    d_dict, t_to_d, p_by_n, existing = {}, defaultdict(list), defaultdict(set), load_semantic_dag(store_path)
    for m in load_store_index(store_path).models: _process_model_semantics(m, project_root, resolve_model_ref, pythonpath, report, d_dict, t_to_d, p_by_n)
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
