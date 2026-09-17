"""Node ids and vocabulary of the edge index (kept from kgdb's typed ingest, id for id)."""

from __future__ import annotations

EDGE_INDEX_VERSION = "1"
STORE_NODE_ID = "sldb://store"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
ANCHOR_TAG = "type.knowledge.anchor"


def doc_node_id(export_id: str) -> str:
    """Node id of a document, from its export id `Model:name` (`store:Model:name` if linked)."""
    return f"sldb://document/{export_id}"


def section_node_id(export_id: str, section_path: str) -> str:
    """Node id of one section of the document `export_id`."""
    return f"sldb://section/{export_id}#{section_path}"


def model_node_id(name: str) -> str:
    """Node id of a registered model."""
    return f"sldb://model/{name}"


def field_node_id(model: str, field: str) -> str:
    """Node id of one field of a model."""
    return f"sldb://field/{model}.{field}"


def tag_node_id(tag: str) -> str:
    """Node id of a semantic tag."""
    return f"sldb://semantic_tag/{tag}"


def relation_type_node_id(name: str) -> str:
    """Node id of a relation type (the `name` of a tracked RelationTypeDoc)."""
    return f"sldb://relation_type/{name}"


def anchor_node_id(symbol: str) -> str:
    """Node id of an anchor (an alias word)."""
    return f"sldb://anchor/{symbol}"


def as_node_id(node_or_export_id: str) -> str:
    """A node id as given; a bare export id (`Model:name`) read as its document's node id."""
    if node_or_export_id.startswith("sldb://"):
        return node_or_export_id
    return doc_node_id(node_or_export_id)
