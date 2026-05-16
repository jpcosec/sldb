from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from sldb.runtime.validation import extract_model_data
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

logger = logging.getLogger(__name__)


@dataclass
class RebuildReport:
    docs_processed: int = 0
    docs_skipped_missing: int = 0
    docs_empty_sections: int = 0
    headings_no_map: int = 0
    verbose: list[str] = field(default_factory=list)


def rebuild_semantic_indexes(
    store_path: Path,
    project_root: Path,
    resolve_model_ref,
    pythonpath: str | None = None,
    report: RebuildReport | None = None,
) -> RebuildReport:
    """Rebuilds the semantic DAG and index for the store."""
    if report is None:
        report = RebuildReport()
    store_index = load_store_index(store_path)
    existing_dag = load_semantic_dag(store_path)
    documents: dict[str, SemanticDocumentRecord] = {}
    tags_to_docs: dict[str, list[str]] = defaultdict(list)
    parents_by_node: dict[str, set[str]] = defaultdict(set)

    for model_entry in store_index.models:
        model_type = resolve_model_ref(model_entry.model_ref, pythonpath)
        models_idx = load_models_index(project_root / model_entry.models_index)
        docs_idx = load_documents_index(project_root / models_idx.documents_index)

        for doc in docs_idx.documents:
            doc_path = project_root / doc.path
            if not doc_path.exists():
                report.docs_skipped_missing += 1
                report.verbose.append(f"semantic: {doc.name} — missing file {doc_path}")
                logger.warning(
                    "Semantic rebuild: doc '%s' missing at %s", doc.name, doc_path
                )
                continue
            report.docs_processed += 1
            try:
                payload = extract_model_data(
                    model_type, doc_path.read_text(encoding="utf-8")
                )
            except Exception:
                payload = {}

            semantic_tags = collect_document_semantic_tags(model_type, payload)
            doc.semantic_tags = semantic_tags
            documents[doc.name] = SemanticDocumentRecord(
                model=model_entry.name,
                path=doc.path,
                tags=semantic_tags,
            )
            for tag in semantic_tags:
                tags_to_docs[tag].append(doc.name)
                for parent, child in _prefix_edges(tag):
                    parents_by_node[child].add(parent)
                    parents_by_node.setdefault(parent, set())

        save_documents_index(project_root / models_idx.documents_index, docs_idx)

    for child, parents in existing_dag.equivalences.items():
        parents_by_node.setdefault(child, set())
        for parent in parents:
            parents_by_node[child].add(parent)
            parents_by_node.setdefault(parent, set())

    _save_indexes(
        store_path,
        parents_by_node,
        existing_dag.equivalences,
        tags_to_docs,
        documents,
    )
    return report


def _save_indexes(store_path, parents_by_node, equivalences, tags_to_docs, documents):
    dag = SemanticDAG(
        nodes=[
            SemanticNode(id=node_id, parents=sorted(parents))
            for node_id, parents in sorted(parents_by_node.items())
        ],
        equivalences=equivalences,
    )
    save_semantic_dag(store_path, dag)
    save_semantic_index(
        store_path,
        SemanticIndex(
            tags={tag: sorted(docs) for tag, docs in sorted(tags_to_docs.items())},
            documents=documents,
        ),
    )


def _about_terms(breadcrumbs: list[str], semantic_tags: list[str]) -> list[str]:
    seen: set[str] = set()
    terms: list[str] = []
    for breadcrumb in breadcrumbs:
        raw = breadcrumb.strip()
        if raw and raw not in seen:
            seen.add(raw)
            terms.append(raw)
        normalized = _slugify(raw).replace("-", " ").strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            terms.append(normalized)
    for tag in semantic_tags:
        if tag not in seen:
            seen.add(tag)
            terms.append(tag)
    return terms


def rebuild_sections_indexes(
    store_path: Path,
    project_root: Path,
    resolve_model_ref,
    pythonpath: str | None = None,
    report: RebuildReport | None = None,
) -> RebuildReport:
    """Build and persist section context index for all tracked documents."""
    if report is None:
        report = RebuildReport()
    store_index = load_store_index(store_path)

    for model_entry in store_index.models:
        model_type = resolve_model_ref(model_entry.model_ref, pythonpath)
        models_idx = load_models_index(project_root / model_entry.models_index)
        docs_idx = load_documents_index(project_root / models_idx.documents_index)
        doc_sections_list: list[DocSections] = []

        for doc in docs_idx.documents:
            doc_path = project_root / doc.path
            if not doc_path.exists():
                report.docs_skipped_missing += 1
                report.verbose.append(f"sections: {doc.name} — missing file {doc_path}")
                logger.warning(
                    "Sections rebuild: doc '%s' missing at %s", doc.name, doc_path
                )
                continue
            report.docs_processed += 1
            markdown = doc_path.read_text(encoding="utf-8")
            sections = _extract_sections(markdown)
            if not sections:
                report.docs_empty_sections += 1
                report.verbose.append(f"sections: {doc.name} — no headings found")
                logger.info("Sections rebuild: doc '%s' has no headings", doc.name)
            semantic_tags = list(doc.semantic_tags) if doc.semantic_tags else []
            section_records: list[SectionContextRecord] = []
            stack: list[tuple[int, list[str]]] = []

            for sec in sections:
                while stack and stack[-1][0] >= sec["level"]:
                    stack.pop()
                breadcrumbs = list(stack[-1][1]) if stack else []
                breadcrumbs.append(sec["title"])
                stack.append((sec["level"], breadcrumbs))
                if sec.get("line_start") is None:
                    report.headings_no_map += 1
                    report.verbose.append(
                        f"sections: {doc.name} — heading '{sec['title']}' has no line map"
                    )
                    logger.warning(
                        "Sections rebuild: heading '%s' in doc '%s' has no line map",
                        sec["title"],
                        doc.name,
                    )
                section_records.append(
                    SectionContextRecord(
                        path=sec["path"],
                        title=sec["title"],
                        breadcrumbs=breadcrumbs,
                        about=_about_terms(breadcrumbs, semantic_tags),
                        semantic_tags=semantic_tags,
                        slug=sec["slug"],
                        level=sec["level"],
                        line_start=sec.get("line_start"),
                        line_end=sec.get("line_end"),
                    )
                )
            doc_sections_list.append(
                DocSections(doc_name=doc.name, sections=section_records)
            )

        if doc_sections_list:
            sections_dir = Path(model_entry.models_index).parent
            sections_path = project_root / sections_dir / "sections_index.yaml"
            save_sections_index(
                sections_path, SectionsIndex(documents=doc_sections_list)
            )
            models_idx.sections_index = str(sections_dir / "sections_index.yaml")
            save_models_index(project_root / model_entry.models_index, models_idx)

    return report


def _extract_sections(markdown: str) -> list[dict]:
    """Extract section headings from markdown."""
    nodes = []
    from markdown_it import MarkdownIt
    from markdown_it.tree import SyntaxTreeNode

    md = MarkdownIt("gfm-like")
    tokens = md.parse(markdown)
    root = SyntaxTreeNode(tokens)
    for child in root.children:
        nodes.append(
            {
                "type": child.type,
                "tag": child.tag,
                "content": (
                    child.children[0].content if child.children else child.content
                )
                or "",
                "map": list(child.map) if child.map else None,
            }
        )

    sections: list[dict] = []
    stack: list[dict] = []
    for node in nodes:
        if not re.fullmatch(r"h[1-6]", node.get("tag") or ""):
            continue
        title = (node.get("content") or "").strip()
        if not title:
            continue
        level = int(node["tag"][1])
        while stack and stack[-1]["level"] >= level:
            stack.pop()
        slug = _slugify(title)
        parent = "/".join(item["slug"] for item in stack)
        path = f"{parent}/{slug}" if parent else slug
        map_vals = node.get("map") or [None, None]
        start = map_vals[0]
        end = map_vals[1]
        sec = {
            "title": title,
            "slug": slug,
            "level": level,
            "path": path,
            "line_start": start + 1 if start is not None else None,
            "line_end": end + 1 if end is not None else None,
        }
        sections.append(sec)
        stack.append(sec)
    return sections


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def add_semantic_equivalence(store_path: Path, local_tag: str, global_tag: str) -> None:
    """Adds a semantic equivalence mapping to the store DAG."""
    dag = load_semantic_dag(store_path)
    mapped = set(dag.equivalences.get(local_tag, []))
    mapped.add(global_tag)
    dag.equivalences[local_tag] = sorted(mapped)
    save_semantic_dag(store_path, dag)
