"""The schema edges of the store's index, projected onto project graph nodes."""

from __future__ import annotations

from typing import Callable

from sldb.api.edges.project_graph.node_lookup import NodeLookup
from sldb.api.edges.project_graph.project_edge import ProjectEdge
from sldb.api.edges.project_graph.project_store import ProjectStore
from sldb.store.models import EdgeRecord

DECLARING_RELATIONS = {"references", "contains"}


def store_edges(store: ProjectStore, lookup: NodeLookup, is_record_path: Callable[[str], bool | None], extractor: str) -> list[ProjectEdge]:
    """Reference and containment edges between two tracked documents that are both project nodes.

    Args:
        store: The project store.
        lookup: The project's nodes.
        is_record_path: Whether the document at a path is an archived record (True or None).
        extractor: Name of the reader, stamped on every edge.

    Returns:
        Edges in index order; the role is the declaring field.
    """
    edges: list[ProjectEdge] = []
    records: dict[str, bool | None] = {}
    for edge in store.index.edges:
        ends = _ends(store, lookup, edge)
        if ends is not None:
            source_path, source_id, target_id, field = ends
            if source_path not in records:
                records[source_path] = is_record_path(source_path)
            edges.append(ProjectEdge(source_id=source_id, target_id=target_id, role=field, provenance_path=source_path, provenance_locator="frontmatter", extractor=extractor, record=records[source_path]))
    return edges


def _ends(store: ProjectStore, lookup: NodeLookup, edge: EdgeRecord) -> tuple[str, str, str, str] | None:
    """(source path, source id, target id, field) of a declared edge whose two ends are nodes."""
    field = (edge.metadata or {}).get("field")
    if not field or edge.relation not in DECLARING_RELATIONS:
        return None
    source_record, target_record = store.index.nodes.get(edge.source), store.index.nodes.get(edge.target)
    if source_record is None or target_record is None:
        return None
    source_path = source_record.semantics.get("path")
    source, target = lookup.by_path.get(source_path), lookup.by_path.get(target_record.semantics.get("path"))
    return None if source is None or target is None else (source_path, source.id, target.id, field)
