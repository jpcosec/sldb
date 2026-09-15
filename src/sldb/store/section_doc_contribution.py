"""A model's section entries, one document at a time, remembered by `hash_c` so a rebuild
only re-parses a document whose text moved (PLAN 15 M2) — the sections counterpart of
`semantic_doc_contribution`, called by `section_rebuild._process_model_sections`."""

from __future__ import annotations

import logging

from sldb.store.io import load_documents_index, save_models_index, save_sections_index
from sldb.store.models import DocSections, SectionsIndex

logger = logging.getLogger(__name__)


def walk_sections(m_entry, m_idx, root, report, process_doc_sections, stale: dict | None = None) -> list:
    """(doc_name, DocSections, hash_c) per tracked document: one whose `hash_c` matches what
    `stale` (this model's last cached sections, key or no key) recorded it as comes back
    unparsed. `process_doc_sections` is section_rebuild's own parser, passed in rather than
    imported back (this module is the one section_rebuild imports)."""
    stale_docs = {e["name"]: e for e in (stale or {}).get("entries", [])}
    out = []
    for doc in load_documents_index(root / m_idx.documents_index).documents:
        d_path = root / doc.path
        if not d_path.exists():
            _missing_doc(doc, d_path, report)
            continue
        out.append(_section_entry(doc, d_path, stale_docs.get(doc.name), report, process_doc_sections))
    return out


def _missing_doc(doc, d_path, report) -> None:
    report.docs_skipped_missing += 1
    report.verbose.append(f"sections: {doc.name} — missing file {d_path}")
    logger.warning(f"Sections rebuild: doc '{doc.name}' missing at {d_path}")


def _section_entry(doc, d_path, cached, report, process_doc_sections) -> tuple:
    if cached is not None and cached.get("hash_c") == doc.hash_c:
        report.docs_processed += 1
        sections = DocSections.model_validate(cached["sections"])
        if not sections.sections:
            report.docs_empty_sections += 1
        return doc.name, sections, doc.hash_c
    return doc.name, process_doc_sections(doc, d_path, report), doc.hash_c


def save_sections(m_entry, m_idx, root, s_rel, entries, store_path, key) -> None:
    if not entries:
        return
    d_sections = [e[1] for e in entries]
    save_sections_index(root / s_rel, SectionsIndex(documents=d_sections))
    m_idx.sections_index = s_rel
    save_models_index(root / m_entry.models_index, m_idx)
    if store_path:
        _cache_sections(store_path, m_entry.name, key, entries, d_sections)


def _cache_sections(store_path, model_name, key, entries, d_sections) -> None:
    from sldb.store import built_cache

    built_cache.put(store_path, "sections", model_name, key, {
        "docs": len(d_sections),
        "empty": sum(1 for d in d_sections if not d.sections),
        "entries": [{"name": n, "hash_c": h, "sections": sec.model_dump()} for n, sec, h in entries],
    })
