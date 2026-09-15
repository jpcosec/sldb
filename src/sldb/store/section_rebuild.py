from __future__ import annotations
import logging
import re
from pathlib import Path

from sldb.store.io import load_models_index, load_store_index
from sldb.store.layout import sections_index_relpath
from sldb.store.models import DocSections, SectionContextRecord
from sldb.store.section_doc_contribution import save_sections as _save_sections, walk_sections as _walk_sections
from sldb.store.semantic import RebuildReport, _about_terms

logger = logging.getLogger(__name__)

def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"

def _parse_md_nodes(markdown: str):
    from markdown_it import MarkdownIt
    from markdown_it.tree import SyntaxTreeNode
    return [{"type": c.type, "tag": c.tag, "content": (c.children[0].content if c.children else c.content) or "", "map": list(c.map) if c.map else None} for c in SyntaxTreeNode(MarkdownIt("gfm-like").parse(markdown)).children]

def _build_section(node, stack):
    title = (node.get("content") or "").strip()
    if not title: return None
    level = int(node["tag"][1])
    while stack and stack[-1]["level"] >= level: stack.pop()
    slug, parent = _slugify(title), "/".join(i["slug"] for i in stack)
    m_vals = node.get("map") or [None, None]
    return {"title": title, "slug": slug, "level": level, "path": f"{parent}/{slug}" if parent else slug, "line_start": m_vals[0] + 1 if m_vals[0] is not None else None, "line_end": m_vals[1] + 1 if m_vals[1] is not None else None}

def _extract_sections(markdown: str) -> list[dict]:
    sections, stack = [], []
    for node in _parse_md_nodes(markdown):
        if not re.fullmatch(r"h[1-6]", node.get("tag") or ""): continue
        sec = _build_section(node, stack)
        if sec: sections.append(sec); stack.append(sec)
    return sections

_DOC_SECTIONS: dict[tuple, list[dict]] = {}   # (path, mtime, size) -> headings; a rebuild only parses what changed


def _file_signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


def _sections_of(d_path: Path, hash_c: str = "") -> list[dict]:
    key = (str(d_path), hash_c) if hash_c else (str(d_path), *_file_signature(d_path))
    secs = _DOC_SECTIONS.get(key)
    if secs is None:
        secs = _DOC_SECTIONS[key] = _extract_sections(d_path.read_text(encoding="utf-8"))
    return secs


def _process_doc_sections(doc, d_path, report):
    report.docs_processed += 1
    if not (secs := _sections_of(d_path, doc.hash_c)): report.docs_empty_sections += 1
    tags, records, stack = list(doc.semantic_tags or []), [], []
    for s in secs:
        while stack and stack[-1][0] >= s["level"]: stack.pop()
        b_crumbs = list(stack[-1][1]) if stack else []
        b_crumbs.append(s["title"]); stack.append((s["level"], b_crumbs))
        if s.get("line_start") is None: report.headings_no_map += 1
        records.append(SectionContextRecord(path=s["path"], title=s["title"], breadcrumbs=b_crumbs, about=_about_terms(b_crumbs, tags), semantic_tags=tags, slug=s["slug"], level=s["level"], line_start=s.get("line_start"), line_end=s.get("line_end")))
    return DocSections(doc_name=doc.name, sections=records)

def _process_model_sections(m_entry, root, report, store_path: Path | None = None):
    from sldb.store import built_cache
    m_idx = load_models_index(root / m_entry.models_index)
    s_rel, key = sections_index_relpath(m_entry.name), built_cache.model_key(m_idx)
    done = built_cache.get(store_path, "sections", m_entry.name, key) if store_path else None
    if done is not None and (root / s_rel).exists() and m_idx.sections_index == s_rel:
        report.docs_processed += done["docs"]; report.docs_empty_sections += done["empty"]; return
    stale = built_cache.get_stale(store_path, "sections", m_entry.name) if store_path else None
    entries = _walk_sections(m_entry, m_idx, root, report, _process_doc_sections, stale=stale)
    _save_sections(m_entry, m_idx, root, s_rel, entries, store_path, key)

def rebuild_sections_indexes(store_path: Path, project_root: Path, resolve_model_ref, pythonpath: str | None = None, report: RebuildReport | None = None) -> RebuildReport:
    report = report or RebuildReport()
    for m in load_store_index(store_path).models: _process_model_sections(m, project_root, report, store_path)
    return report

