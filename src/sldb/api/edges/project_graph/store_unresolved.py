"""Values the store's index leaves unresolved that are dangling in the project graph too."""

from __future__ import annotations

from sldb.api.edges.project_graph.node_lookup import NodeLookup, ProjectNode
from sldb.api.edges.project_graph.project_store import ProjectStore
from sldb.api.edges.project_graph.store_edges import DECLARING_RELATIONS
from sldb.store.edge_index.unresolved_reference import UnresolvedReference


def store_unresolved(store: ProjectStore, lookup: NodeLookup, provenance_fields: tuple[str, ...]) -> list[tuple[UnresolvedReference, str, ProjectNode]]:
    """(reference, value, declaring node) of each unresolved value that names no project node either.

    sldb resolves against its tracked documents; the project graph also has nodes for
    untracked files, so a value naming one of those is not dangling. Prose in a declared
    field is no reference, and a provenance field never dangles.

    Args:
        store: The project store.
        lookup: The project's nodes.
        provenance_fields: Fields whose values are history, not references.

    Returns:
        The dangling values in index order.
    """
    found: list[tuple[UnresolvedReference, str, ProjectNode]] = []
    for reference in store.index.unresolved_references:
        value = (reference.target or "").strip()
        if not _dangles(reference, value, lookup, provenance_fields):
            continue
        source = _source_node(reference, lookup)
        if source is not None:
            found.append((reference, value, source))
    return found


def _dangles(reference: UnresolvedReference, value: str, lookup: NodeLookup, provenance_fields: tuple[str, ...]) -> bool:
    if reference.relation not in DECLARING_RELATIONS or reference.field in provenance_fields:
        return False
    return lookup.looks_like_reference(value) and not _resolves(reference, value, lookup)


def _resolves(reference: UnresolvedReference, value: str, lookup: NodeLookup) -> bool:
    if reference.target_export_id and reference.target_export_id.split(":", 1)[-1] in lookup.ids_by_name:
        return True
    if value.strip("`").removeprefix("./") in lookup.by_path:
        return True
    resolved = lookup.reference_id(value)
    return bool(resolved and resolved in lookup.existing_ids)


def _source_node(reference: UnresolvedReference, lookup: NodeLookup) -> ProjectNode | None:
    node = lookup.by_path.get((reference.source_path or "").removeprefix("./"))
    if node is not None:
        return node
    node_id = lookup.ids_by_name.get(reference.source.split(":", 1)[-1])
    return lookup.by_id.get(node_id) if node_id else None
