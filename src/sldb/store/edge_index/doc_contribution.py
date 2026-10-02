"""One document's whole contribution to the edge index, ready to be its shard."""

from __future__ import annotations

from typing import Any, Callable

from sldb.store.edge_index.composition_edges import composition_edges
from sldb.store.edge_index.declared_references import declared_reference_edges
from sldb.store.edge_index.doc_kinds import special_contribution
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.edge_index.doc_structure import document_structure
from sldb.store.edge_index.records import tag_nodes
from sldb.store.models import DocEdges, DocumentEntry, SectionContextRecord


def build_doc_edges(model_name: str, doc: DocumentEntry, sections: list[SectionContextRecord], payload_of: Callable[[], dict[str, Any] | None], model_type: Any | None = None) -> DocEdges:
    """A relation type, relation or anchor document contributes what it declares; any other
    document contributes itself, its sections, and the references its model declares. Either
    way its tags become nodes: a tag exists in the index because some document, model or DAG
    entry carries it.

    Args:
        model_name: Model the document is tracked under.
        doc: The document's index entry (name, path, hashes, tags).
        sections: The document's sections, from its sections shard.
        payload_of: Reads the document's field payload; called for the special kinds and for
            any model that declares `__references__`, `__containment__` or `__compositions__`.
        model_type: The imported model class, or None when it cannot be imported; without it
            no declared reference is read, as in `build_model_edges`.

    Returns:
        The shard, not yet stamped with `source_hash` / `edges_version` (the caller's cache keys).
    """
    special = special_contribution(model_name, doc, payload_of)
    part = special or document_structure(model_name, doc, sections)
    edges = part.edges + _declared_edges(model_name, doc, model_type, payload_of, special is not None)
    tags = set(doc.semantic_tags).union(*(s.semantic_tags for s in sections))
    return DocEdges(doc_name=doc.name, model_name=model_name, semantic_tags=sorted(set(doc.semantic_tags)), nodes=part.nodes + tag_nodes(tags), edges=edges)


def _declared_edges(model_name: str, doc: DocumentEntry, model_type: Any | None, payload_of: Callable[[], dict[str, Any] | None], is_special: bool):
    """The model's declared references, read only when it declares any: the payload is a file
    read per document, and most models declare none.

    A relation, relation type or anchor document is skipped: its id fields are the edge it
    already contributes (`RelationDoc.__references__` names the ends of that very edge), so
    reading them again would assert a second, untyped edge beside it.
    """
    if is_special or model_type is None:
        return []
    if not _declares_links(model_type):
        return []
    payload = payload_of()
    references = declared_reference_edges(model_name, doc.name, model_type, payload)
    return references + composition_edges(doc_node_id(f"{model_name}:{doc.name}"), model_type, payload)


def _declares_links(model_type: Any) -> bool:
    """Whether the model names other documents at all: otherwise its payload is not read."""
    dunders = ("__references__", "__containment__", "__compositions__")
    return any(getattr(model_type, name, None) for name in dunders)
