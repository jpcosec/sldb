"""One document's whole contribution to the edge index, ready to be its shard."""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.edge_index.doc_kinds import special_contribution
from sldb.store.edge_index.doc_structure import document_structure
from sldb.store.edge_index.records import tag_nodes
from sldb.store.models import DocEdges, DocumentEntry, SectionContextRecord


def build_doc_edges(model_name: str, doc: DocumentEntry, sections: list[SectionContextRecord], payload_of: Callable[[], dict[str, Any] | None]) -> DocEdges:
    """A relation type, relation or anchor document contributes what it declares; any other
    document contributes itself and its sections. Either way its tags become nodes: a tag
    exists in the index because some document, model or DAG entry carries it.

    Args:
        model_name: Model the document is tracked under.
        doc: The document's index entry (name, path, hashes, tags).
        sections: The document's sections, from its sections shard.
        payload_of: Reads the document's field payload; only called for the special kinds.

    Returns:
        The shard, not yet stamped with `hash_c` / `edges_version` (the caller's cache keys).
    """
    part = special_contribution(model_name, doc, payload_of) or document_structure(model_name, doc, sections)
    tags = set(doc.semantic_tags).union(*(s.semantic_tags for s in sections))
    return DocEdges(doc_name=doc.name, model_name=model_name, semantic_tags=sorted(set(doc.semantic_tags)), nodes=part.nodes + tag_nodes(tags), edges=part.edges)
