import re
from typing import Any
from sldb.core.ir import SourceSpan, SurfaceNode
from sldb.api.schema.field_kinds import annotation_name as _annotation_name  # noqa: F401 - moved to sldb.api.schema

def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"

def _to_surface_node(node: Any) -> SurfaceNode:
    return SurfaceNode(
        kind=node.type, text=node.content,
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
    _add_breadcrumbs(breadcrumbs, seen, terms)
    _add_tags(semantic_tags, seen, terms)
    return terms

def _add_breadcrumbs(breadcrumbs: list[str], seen: set[str], terms: list[str]):
    for breadcrumb in breadcrumbs:
        raw = breadcrumb.strip()
        if raw and raw not in seen:
            seen.add(raw); terms.append(raw)
        normalized = _slugify(raw).replace("-", " ").strip()
        if normalized and normalized not in seen:
            seen.add(normalized); terms.append(normalized)

def _add_tags(semantic_tags: list[str], seen: set[str], terms: list[str]):
    for tag in semantic_tags:
        if tag not in seen:
            seen.add(tag)
            terms.append(tag)
