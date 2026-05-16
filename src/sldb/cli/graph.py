from __future__ import annotations

import difflib
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

from sldb.cli.utils import get_store_context, resolve_model_ref
from sldb.core.ast import AST_Handler
from sldb.core.contracts import MARKER_PATTERN, parse_marker
from sldb.core.ir import (
    DocumentContext,
    DocumentIR,
    GraphEdge,
    GraphView,
    MeaningNode,
    SectionContextEntry,
    SourceSpan,
    SurfaceNode,
)
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_sections_index,
    load_store_index,
)
from sldb.store.models import DocSections, SectionContextRecord, SectionsIndex
from sldb.store.query import load_runtime_documents


@dataclass
class SectionRecord:
    title: str
    slug: str
    level: int
    path: str
    line_start: int | None
    line_end: int | None


@dataclass
class SearchRecord:
    kind: str
    store_name: str
    name: str
    physical: list[str]
    semantic: list[str]
    payload: dict[str, Any]
    value: Any = None
    model_name: str | None = None
    doc_name: str | None = None
    field_path: str | None = None
    path: str | None = None
    title: str | None = None
    about: list[str] | None = None
    owning_section: str | None = None

    def as_dict(self) -> dict[str, Any]:
        d = {
            "kind": self.kind,
            "store": self.store_name,
            "name": self.name,
            "model": self.model_name,
            "doc": self.doc_name,
            "field": self.field_path,
            "path": self.path,
            "title": self.title,
            "value": self.value,
            "semantic": self.semantic,
            "about": self.about or [],
        }
        if self.kind == "section":
            d["breadcrumbs"] = self.payload.get("breadcrumbs", [])
        if self.kind == "field":
            d["owning_section"] = self.owning_section
        return d


def extract_sections(markdown: str) -> list[SectionRecord]:
    nodes = AST_Handler().split_nodes(markdown)
    sections: list[SectionRecord] = []
    stack: list[SectionRecord] = []

    for node in nodes:
        if not re.fullmatch(r"h[1-6]", node.tag or ""):
            continue
        title = (node.find_leaf_text() or node.content or "").strip()
        if not title:
            continue
        level = int(node.tag[1])
        while stack and stack[-1].level >= level:
            stack.pop()
        slug = _slugify(title)
        parent = "/".join(item.slug for item in stack)
        path = f"{parent}/{slug}" if parent else slug
        start = node.map[0] + 1 if node.map else None
        end = node.map[1] + 1 if node.map else None
        section = SectionRecord(
            title=title,
            slug=slug,
            level=level,
            path=path,
            line_start=start,
            line_end=end,
        )
        sections.append(section)
        stack.append(section)

    return sections


def flatten_payload(payload: Any, prefix: str = "") -> list[tuple[str, Any]]:
    if isinstance(payload, dict):
        pairs: list[tuple[str, Any]] = []
        for key, value in payload.items():
            path = f"{prefix}.{key}" if prefix else key
            pairs.extend(flatten_payload(value, path))
        return pairs
    return [(prefix, payload)]


def build_store_ast(
    store_arg: str | None, pythonpath: str | None, include_linked: bool = False
) -> dict[str, Any]:
    store_path, root = get_store_context(store_arg)
    store_index = load_store_index(store_path)

    linked = [
        {"name": entry.name, "path": entry.path}
        for entry in sorted(store_index.stores, key=lambda item: item.name)
    ]

    models: list[dict[str, Any]] = []
    for entry in sorted(store_index.models, key=lambda item: item.name):
        model_type = resolve_model_ref(entry.model_ref, pythonpath)
        models_index = load_models_index(root / entry.models_index)
        docs_index = load_documents_index(root / models_index.documents_index)
        fields = []
        for field_name, field in model_type.model_fields.items():
            fields.append(
                {
                    "name": field_name,
                    "annotation": _annotation_name(field.annotation),
                    "description": field.description or "",
                }
            )
        documents = [
            {
                "name": doc.name,
                "path": doc.path,
                "semantic_tags": list(doc.semantic_tags),
            }
            for doc in sorted(docs_index.documents, key=lambda item: item.name)
        ]
        models.append(
            {
                "name": entry.name,
                "model_ref": entry.model_ref,
                "path": entry.path,
                "canonical": getattr(models_index, "canonical", False),
                "family": getattr(models_index, "family", None),
                "semantics": list(getattr(models_index, "semantics", [])),
                "base_models": list(getattr(models_index, "base_models", [])),
                "fields": fields,
                "documents": documents,
            }
        )

    ast: dict[str, Any] = {
        "store": {
            "path": str(store_path),
            "root": str(root),
            "linked_stores": linked,
            "models": models,
        }
    }

    if include_linked:
        ast["linked_documents"] = [
            {
                "store": doc.store_name,
                "model": doc.model_name,
                "doc": doc.name,
                "path": doc.path,
                "semantic_tags": doc.semantic_tags,
            }
            for doc in load_runtime_documents(
                store_path, resolve_model_ref, pythonpath, include_linked=True
            )
            if doc.store_name != "local"
        ]

    return ast


def ast_for_target(
    store_arg: str | None, pythonpath: str | None, target: str
) -> dict[str, Any]:
    graph = build_store_ast(store_arg, pythonpath)
    store = graph["store"]
    target = (target or "store").strip("/")
    if target in {"", "store", "stores"}:
        return graph

    if target.startswith("models/"):
        model_name = target.split("/", 1)[1]
        model = next(
            (item for item in store["models"] if item["name"] == model_name), None
        )
        if model is None:
            raise ValueError(f"Unknown model target: {target}")
        return {"model": model}

    if target.startswith("docs/"):
        doc_ref = target.split("/", 1)[1]
        runtime_doc = resolve_runtime_doc(store_arg, doc_ref, pythonpath)
        markdown = Path(runtime_doc["absolute_path"]).read_text(encoding="utf-8")
        ir = build_document_ir(
            runtime_doc, markdown, template=runtime_doc.get("template")
        )
        return {
            "document": {
                "store": runtime_doc["store"],
                "model": runtime_doc["model"],
                "name": runtime_doc["name"],
                "path": runtime_doc["path"],
                "semantic_tags": runtime_doc["semantic_tags"],
                "payload": runtime_doc["payload"],
                "sections": [
                    section.__dict__ for section in extract_sections(markdown)
                ],
                "ir": ir.model_dump(mode="json"),
            }
        }

    if target.startswith("fields/"):
        field_ref = target.split("/", 1)[1]
        docs = query_field_records(
            store_arg, pythonpath, field_ref, include_linked=False
        )
        return {"field": {"target": field_ref, "matches": docs}}

    raise ValueError(f"Unknown ast target: {target}")


def resolve_runtime_doc(
    store_arg: str | None, doc_ref: str, pythonpath: str | None
) -> dict[str, Any]:
    store_path, root = get_store_context(store_arg)
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    candidates = []
    normalized = doc_ref.strip("/")
    for doc in docs:
        physical = [doc.name, doc.path, f"{doc.model_name}/{doc.name}"]
        if normalized in physical:
            candidates.append(doc)
    if not candidates:
        raise ValueError(f"Unknown document target: {doc_ref}")
    if len(candidates) > 1:
        raise ValueError(
            f"Ambiguous document target '{doc_ref}'. Use 'Model/DocName' or a tracked path."
        )
    doc = candidates[0]
    template: str | None = getattr(doc.model_type, "__template__", None)
    return {
        "store": doc.store_name,
        "model": doc.model_name,
        "name": doc.name,
        "path": doc.path,
        "absolute_path": str((root / doc.path).resolve()),
        "payload": doc.payload,
        "semantic_tags": doc.semantic_tags,
        "template": template,
    }


def query_field_records(
    store_arg: str | None,
    pythonpath: str | None,
    field_ref: str,
    include_linked: bool = False,
) -> list[dict[str, Any]]:
    store_path, root = get_store_context(store_arg)
    store_index = load_store_index(store_path)
    docs = load_runtime_documents(
        store_path, resolve_model_ref, pythonpath, include_linked=include_linked
    )

    model_sections: dict[str, SectionsIndex] = {}
    for model_entry in store_index.models:
        models_idx = load_models_index(root / model_entry.models_index)
        if models_idx.sections_index:
            sections_path = root / models_idx.sections_index
            model_sections[model_entry.name] = load_sections_index(sections_path)

    results = []
    for doc in docs:
        matched_pairs = [
            (path, value)
            for path, value in flatten_payload(doc.payload)
            if path == field_ref or path.endswith(f".{field_ref}")
        ]
        if not matched_pairs:
            continue

        owning_section_map: dict[str, str | None] = {}
        doc_template: str | None = getattr(doc.model_type, "__template__", None)

        if doc_template:
            sections_idx = model_sections.get(doc.model_name)
            doc_sections = None
            if sections_idx is not None:
                doc_sections = next(
                    (ds for ds in sections_idx.documents if ds.doc_name == doc.name),
                    None,
                )
            if doc_sections is not None and doc_sections.sections:
                owning_section_map = _map_fields_to_sections(
                    doc_template, doc_sections.sections
                )
            else:
                doc_path = doc.store_path.parent / doc.path
                if doc_path.exists():
                    markdown = doc_path.read_text(encoding="utf-8")
                    sections = extract_sections(markdown)
                    owning_section_map = _map_fields_to_sections(doc_template, sections)

        for path, value in matched_pairs:
            results.append(
                {
                    "store": doc.store_name,
                    "model": doc.model_name,
                    "doc": doc.name,
                    "path": doc.path,
                    "field": path,
                    "value": value,
                    "owning_section": owning_section_map.get(path),
                }
            )
    return results


def iter_search_records(
    store_arg: str | None,
    pythonpath: str | None,
    include_linked: bool = False,
    rebuild: bool = False,
) -> list[SearchRecord]:
    store_path, root = get_store_context(store_arg)
    store_index = load_store_index(store_path)
    runtime_docs = load_runtime_documents(
        store_path, resolve_model_ref, pythonpath, include_linked=include_linked
    )

    model_sections: dict[str, SectionsIndex] = {}
    if not rebuild:
        for model_entry in store_index.models:
            models_idx = load_models_index(root / model_entry.models_index)
            if models_idx.sections_index:
                sections_path = root / models_idx.sections_index
                model_sections[model_entry.name] = load_sections_index(sections_path)

    local_models = {entry.name: entry for entry in store_index.models}
    records: list[SearchRecord] = [
        SearchRecord(
            kind="store",
            store_name="local",
            name="local",
            physical=[str(store_path), str(root), ".sldb"],
            semantic=[],
            payload={
                "linked_count": len(store_index.stores),
                "model_count": len(store_index.models),
            },
            path=str(store_path),
        )
    ]
    records.extend(
        SearchRecord(
            kind="store",
            store_name="local",
            name=entry.name,
            physical=[entry.name, entry.path],
            semantic=[],
            payload={"linked": True},
            path=entry.path,
        )
        for entry in store_index.stores
    )

    seen_models: set[tuple[str, str]] = set()
    for doc in runtime_docs:
        model_key = (doc.store_name, doc.model_name)
        if model_key not in seen_models:
            entry = local_models.get(doc.model_name)
            semantics = list(getattr(entry, "semantics", [])) if entry else []
            records.append(
                SearchRecord(
                    kind="model",
                    store_name=doc.store_name,
                    name=doc.model_name,
                    physical=[
                        doc.model_name,
                        getattr(doc.model_type, "__module__", ""),
                    ],
                    semantic=semantics,
                    payload={"field_count": len(doc.model_type.model_fields)},  # type: ignore[attr-defined]
                    model_name=doc.model_name,
                    path=getattr(entry, "path", None) if entry else None,
                )
            )
            seen_models.add(model_key)

        records.append(
            SearchRecord(
                kind="doc",
                store_name=doc.store_name,
                name=doc.name,
                physical=[doc.name, doc.path, f"{doc.model_name}/{doc.name}"],
                semantic=list(doc.semantic_tags),
                payload=doc.payload,
                model_name=doc.model_name,
                doc_name=doc.name,
                path=doc.path,
            )
        )

        doc_path = Path(doc.store_path.parent / doc.path)
        if doc_path.exists():
            doc_template: str | None = getattr(doc.model_type, "__template__", None)

            sections_idx = model_sections.get(doc.model_name)
            doc_sections = None
            if sections_idx is not None:
                doc_sections = next(
                    (ds for ds in sections_idx.documents if ds.doc_name == doc.name),
                    None,
                )

            if doc_sections is not None and doc_sections.sections:
                for sec in doc_sections.sections:
                    slug = sec.slug or _slugify(sec.title)
                    records.append(
                        SearchRecord(
                            kind="section",
                            store_name=doc.store_name,
                            name=slug,
                            physical=[sec.title, slug, sec.path, doc.path],
                            semantic=list(doc.semantic_tags),
                            payload={
                                "level": sec.level,
                                "line_start": sec.line_start,
                                "line_end": sec.line_end,
                                "breadcrumbs": list(sec.breadcrumbs),
                            },
                            model_name=doc.model_name,
                            doc_name=doc.name,
                            path=f"{doc.path}#{sec.path}",
                            title=sec.title,
                            about=list(sec.about),
                        )
                    )

                known = set(name for name, _ in flatten_payload(doc.payload))
                field_section_map = (
                    _map_fields_to_sections(
                        doc_template,
                        doc_sections.sections,
                        known_fields=known,
                    )
                    if doc_template
                    else {}
                )
                for field_path, value in flatten_payload(doc.payload):
                    records.append(
                        SearchRecord(
                            kind="field",
                            store_name=doc.store_name,
                            name=field_path,
                            physical=[
                                field_path,
                                doc.name,
                                doc.path,
                                doc.model_name,
                            ],
                            semantic=list(doc.semantic_tags),
                            payload=doc.payload,
                            value=value,
                            model_name=doc.model_name,
                            doc_name=doc.name,
                            field_path=field_path,
                            path=f"{doc.path}:{field_path}",
                            owning_section=field_section_map.get(field_path),
                        )
                    )
            else:
                if doc_sections is None:
                    logger.warning(
                        "No persisted sections for '%s', rebuilding IR from markdown",
                        doc.name,
                    )
                ir = build_document_ir(
                    {
                        "store": doc.store_name,
                        "model": doc.model_name,
                        "name": doc.name,
                        "path": doc.path,
                        "payload": doc.payload,
                        "semantic_tags": doc.semantic_tags,
                    },
                    doc_path.read_text(encoding="utf-8"),
                    template=doc_template,
                )
                context_by_path = {
                    entry.path: entry.model_dump(mode="json")
                    for entry in ir.context_index
                }
                field_section_map: dict[str, str | None] = {
                    node.field_path: node.owning_section
                    for node in ir.nodes
                    if node.kind == "field" and node.field_path
                }
                for section in extract_sections(doc_path.read_text(encoding="utf-8")):
                    context_entry = context_by_path.get(section.path, {})
                    records.append(
                        SearchRecord(
                            kind="section",
                            store_name=doc.store_name,
                            name=section.slug,
                            physical=[
                                section.title,
                                section.slug,
                                section.path,
                                doc.path,
                            ],
                            semantic=list(doc.semantic_tags),
                            payload={
                                "level": section.level,
                                "line_start": section.line_start,
                                "line_end": section.line_end,
                                "breadcrumbs": context_entry.get("breadcrumbs", []),
                            },
                            model_name=doc.model_name,
                            doc_name=doc.name,
                            path=f"{doc.path}#{section.path}",
                            title=section.title,
                            about=context_entry.get("about", []),
                        )
                    )

                for field_path, value in flatten_payload(doc.payload):
                    records.append(
                        SearchRecord(
                            kind="field",
                            store_name=doc.store_name,
                            name=field_path,
                            physical=[
                                field_path,
                                doc.name,
                                doc.path,
                                doc.model_name,
                            ],
                            semantic=list(doc.semantic_tags),
                            payload=doc.payload,
                            value=value,
                            model_name=doc.model_name,
                            doc_name=doc.name,
                            field_path=field_path,
                            path=f"{doc.path}:{field_path}",
                            owning_section=field_section_map.get(field_path),
                        )
                    )
        else:
            for field_path, value in flatten_payload(doc.payload):
                records.append(
                    SearchRecord(
                        kind="field",
                        store_name=doc.store_name,
                        name=field_path,
                        physical=[field_path, doc.name, doc.path, doc.model_name],
                        semantic=list(doc.semantic_tags),
                        payload=doc.payload,
                        value=value,
                        model_name=doc.model_name,
                        doc_name=doc.name,
                        field_path=field_path,
                        path=f"{doc.path}:{field_path}",
                    )
                )
    return records


def search_records(
    records: list[SearchRecord],
    term: str,
    search_in: str,
    regex: bool = False,
    fuzzy: bool = False,
    kinds: set[str] | None = None,
) -> list[SearchRecord]:
    if term in {"stores", "models", "docs", "sections", "fields"}:
        kind = term[:-1] if term.endswith("s") else term
        return [record for record in records if record.kind == kind]

    if kinds:
        records = [record for record in records if record.kind in kinds]

    if not term:
        return records

    matched = []
    for record in records:
        haystacks: list[str] = []
        if search_in in {"physical", "both"}:
            haystacks.extend(record.physical)
        if search_in in {"semantic", "both"}:
            haystacks.extend(record.semantic)
            haystacks.extend(record.about or [])
        haystacks = [value for value in haystacks if value]
        if _matches_term(haystacks, term, regex=regex, fuzzy=fuzzy):
            matched.append(record)
    return matched


def _matches_term(haystacks: list[str], term: str, regex: bool, fuzzy: bool) -> bool:
    if regex:
        return any(re.search(term, value) is not None for value in haystacks)
    if fuzzy:
        target = term.lower()
        return any(
            difflib.SequenceMatcher(a=target, b=value.lower()).ratio() >= 0.7
            or target in value.lower()
            for value in haystacks
        )
    return any(term == value or term in value for value in haystacks)


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def _annotation_name(annotation: Any) -> str:
    if annotation is None:
        return "Any"
    if isinstance(annotation, str):
        return annotation
    return getattr(annotation, "__name__", repr(annotation))


def _field_template_line_map(
    markdown: str, known_fields: set[str] | None = None
) -> dict[str, int]:
    """Map field paths to 1-based line numbers from template markers.

    Uses the canonical ``MARKER_PATTERN`` and ``parse_marker`` so that marker
    syntax changes are reflected here automatically.
    """
    field_lines: dict[str, int] = {}
    for line_no, line in enumerate(markdown.split("\n"), 1):
        for match in re.finditer(MARKER_PATTERN, line):
            inner = match.group(1)
            marker = parse_marker(inner)
            if marker.kind not in ("rev", "optrev") or not marker.name:
                continue
            if known_fields is not None and marker.name not in known_fields:
                logger.warning(
                    "Template marker '%s' references unknown field '%s'",
                    match.group(0),
                    marker.name,
                )
            field_lines[marker.name] = line_no
    return field_lines


def _map_fields_to_sections(
    template: str, sections: list, known_fields: set[str] | None = None
) -> dict[str, str]:
    """Map field paths to owning section paths via heading-based ownership.

    A field marker belongs to the nearest preceding heading, regardless of level.
    """
    field_lines = _field_template_line_map(template, known_fields=known_fields)
    heading_lines = sorted(
        (sec.line_start, sec.path) for sec in sections if sec.line_start is not None
    )
    result: dict[str, str] = {}
    for field_path, line_no in field_lines.items():
        owning = None
        for heading_line, section_path in heading_lines:
            if heading_line <= line_no:
                owning = section_path
        if owning is not None:
            result[field_path] = owning
    return result


def build_document_ir(
    runtime_doc: dict[str, Any],
    markdown: str,
    template: str | None = None,
) -> DocumentIR:
    sections = extract_sections(markdown)
    surface = [_to_surface_node(node) for node in AST_Handler().split_nodes(markdown)]
    structure: list[MeaningNode] = []
    section_nodes: list[MeaningNode] = []
    context_index: list[SectionContextEntry] = []
    stack: list[tuple[int, MeaningNode]] = []
    breadcrumb_stack: list[tuple[int, list[str]]] = []

    for section in sections:
        node = MeaningNode(
            kind="section",
            name=section.path,
            title=section.title,
            model=runtime_doc["model"],
            span=SourceSpan(line_start=section.line_start, line_end=section.line_end),
            metadata={"level": section.level, "slug": section.slug},
        )
        while stack and stack[-1][0] >= section.level:
            stack.pop()
        while breadcrumb_stack and breadcrumb_stack[-1][0] >= section.level:
            breadcrumb_stack.pop()
        if stack:
            stack[-1][1].children.append(node)
        else:
            structure.append(node)
        stack.append((section.level, node))
        section_nodes.append(node)
        breadcrumbs = [] if not breadcrumb_stack else list(breadcrumb_stack[-1][1])
        breadcrumbs.append(section.title)
        breadcrumb_stack.append((section.level, breadcrumbs))
        context_index.append(
            SectionContextEntry(
                node_id=f"section:{section.path}",
                path=section.path,
                title=section.title,
                breadcrumbs=breadcrumbs,
                about=_about_terms(breadcrumbs, runtime_doc["semantic_tags"]),
                semantic_tags=list(runtime_doc["semantic_tags"]),
                span=SourceSpan(
                    line_start=section.line_start,
                    line_end=section.line_end,
                ),
            )
        )

    known = set(name for name, _ in flatten_payload(runtime_doc["payload"]))
    field_section_map = _map_fields_to_sections(template or markdown, sections, known_fields=known)
    field_nodes = [
        MeaningNode(
            kind="field",
            name=f"field:{field_path}",
            model=runtime_doc["model"],
            field_path=field_path,
            value=value,
            owning_section=field_section_map.get(field_path),
        )
        for field_path, value in flatten_payload(runtime_doc["payload"])
    ]

    doc_id = f"doc:{runtime_doc['name']}"
    graph = GraphView(
        nodes=[
            {
                "id": doc_id,
                "kind": "document",
                "name": runtime_doc["name"],
                "model": runtime_doc["model"],
            }
        ],
        edges=[],
    )
    for section in section_nodes:
        graph.nodes.append(
            {"id": f"section:{section.name}", "kind": "section", "title": section.title}
        )
        graph.edges.append(
            GraphEdge(
                source=doc_id, target=f"section:{section.name}", relation="has_section"
            )
        )
    for field in field_nodes:
        graph.nodes.append(
            {"id": field.name, "kind": "field", "field_path": field.field_path}
        )
        graph.edges.append(
            GraphEdge(source=doc_id, target=field.name, relation="has_field")
        )

    return DocumentIR(
        context=DocumentContext(
            physical={"store": runtime_doc["store"], "path": runtime_doc["path"]},
            semantic={
                "model": runtime_doc["model"],
                "tags": runtime_doc["semantic_tags"],
            },
        ),
        structure=structure,
        nodes=field_nodes,
        surface=surface,
        graph=graph,
        context_index=context_index,
    )


def _to_surface_node(node: Any) -> SurfaceNode:
    return SurfaceNode(
        kind=node.type,
        text=node.content,
        span=SourceSpan(
            line_start=node.map[0] + 1 if node.map else None,
            line_end=node.map[1] + 1 if node.map else None,
        ),
        children=[_to_surface_node(child) for child in node.children],
        metadata={"tag": node.tag},
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
