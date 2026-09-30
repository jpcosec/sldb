"""Every document-to-document edge of a store, current with its documents."""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.document_edge import DocumentEdge
from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.store.models.edge_record import EdgeRecord

_DOCUMENT_PREFIX = "sldb://document/"


def document_edges(store: str | Path | None, pythonpath: str | None = None, doc_id: str | None = None) -> list[DocumentEdge]:
    """Rebuild the edge index, then list the edges that join two documents.

    Edges with a non-document end (tags, models, fields, the store) are left out.
    Authored edges the index rejected stay out too: they are `EdgeIndex.problems`,
    reported by `check_edges`, and never break this read.

    Args:
        store: The store (path, alias, or None to discover it).
        pythonpath: Directory to import the store's model modules from.
        doc_id: Only edges where this document (`Model:name`) is source or target.

    Returns:
        The edges in the index's stable order.
    """
    rebuild_edges(store, pythonpath, wait=True)
    records = load_edge_index(store, include_linked=False).edges
    edges = [edge for edge in map(_as_document_edge, records) if edge is not None]
    return [edge for edge in edges if doc_id in (None, edge.source, edge.target)]


def _as_document_edge(record: EdgeRecord) -> DocumentEdge | None:
    if not (record.source.startswith(_DOCUMENT_PREFIX) and record.target.startswith(_DOCUMENT_PREFIX)):
        return None
    source, target = record.source[len(_DOCUMENT_PREFIX):], record.target[len(_DOCUMENT_PREFIX):]
    relation_doc = record.metadata.get("relation_doc")
    return DocumentEdge(id=relation_doc or f"{record.relation}:{source}>{target}", source=source, target=target, type=record.relation, origin=str(record.metadata.get("origin", "")), relation_doc=relation_doc)
