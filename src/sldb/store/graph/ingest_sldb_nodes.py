"""Node builders of the semantic export conversion."""

from __future__ import annotations

from typing import Any

from sldb.store.graph.edge import Edge
from sldb.store.graph.identity import SystemIdentity
from sldb.store.graph.node import KnowledgeNode


def _store_node(payload, store_node_id, provenance):
    """The store node, with `has_model` edges to every model."""
    store = payload["store"]
    edges = [Edge(target_id=_model_id(m["name"]), relation_type="has_model") for m in payload["models"]]
    return KnowledgeNode(identity=SystemIdentity(node_id=store_node_id, node_type="sldb_store"), edges=edges, semantics={"root": store["root"], "store_path": store["store_path"], "hash_a": store["hash_a"]}, source=provenance)


def _semantic_tag_node(tag, payload, provenance):
    """A semantic tag node, with `semantic_parent` and `semantic_equivalent` edges."""
    edges = [_edge(_semantic_tag_id(p), "semantic_parent") for p in _parents_of(payload, tag)]
    edges += [_edge(_semantic_tag_id(e), "semantic_equivalent") for e in _equivalents_of(payload, tag)]
    return KnowledgeNode(identity=SystemIdentity(node_id=_semantic_tag_id(tag), node_type="semantic_tag"), edges=edges, semantics={"tag": tag}, source=provenance)


def _model_node(model, documents, store_node_id, provenance):
    """A model node, with `has_document` and `tagged_as` edges."""
    edges = [Edge(target_id=_document_id(d["id"]), relation_type="has_document") for d in documents]
    edges += [Edge(target_id=_semantic_tag_id(t), relation_type="tagged_as") for t in model["semantics"]]
    return KnowledgeNode(identity=SystemIdentity(node_id=_model_id(model["name"]), node_type="sldb_model"), edges=edges, semantics=_model_semantics(model), source={**provenance, "model": model, "parent_store_node_id": store_node_id})


def _document_node(document, sections, provenance):
    """A document node, with `has_section` and `tagged_as` edges."""
    edges = [Edge(target_id=_section_id(s["id"]), relation_type="has_section") for s in sections]
    edges += [Edge(target_id=_semantic_tag_id(t), relation_type="tagged_as") for t in document["semantic_tags"]]
    return KnowledgeNode(identity=SystemIdentity(node_id=_document_id(document["id"]), node_type="sldb_document"), edges=edges, semantics=_document_semantics(document), source={**provenance, "document": document})


def _section_node(section, provenance):
    """A section node, with `tagged_as` edges."""
    edges = [Edge(target_id=_semantic_tag_id(t), relation_type="tagged_as") for t in section["semantic_tags"]]
    return KnowledgeNode(identity=SystemIdentity(node_id=_section_id(section["id"]), node_type="sldb_section"), edges=edges, semantics=_section_semantics(section), source={**provenance, "section": section})


def _edge(target, relation):
    return Edge(target_id=target, relation_type=relation)


def _parents_of(payload, tag):
    for node in payload["semantic_dag"]["nodes"]:
        if node["id"] == tag:
            return node["parents"]
    return []


def _equivalents_of(payload, tag):
    return payload["semantic_dag"]["equivalences"].get(tag, [])


def _model_semantics(model):
    return {"name": model["name"], "model_ref": model["model_ref"], "path": model["path"], "version": model["version"], "canonical": model["canonical"], "family": model.get("family"), "semantic_tags": model["semantics"], "base_models": model["base_models"], "hash_b": model["hash_b"]}


def _document_semantics(document):
    return {"export_id": document["id"], "name": document["name"], "model": document["model"], "path": document["path"], "semantic_tags": document["semantic_tags"], "hash_c": document["hash_c"], "hash_d": document["hash_d"]}


def _section_semantics(section):
    return {"export_id": section["id"], "document_id": section["document_id"], "path": section["path"], "title": section["title"], "breadcrumbs": section["breadcrumbs"], "about": section["about"], "semantic_tags": section["semantic_tags"], "slug": section["slug"], "level": section["level"], "line_start": section.get("line_start"), "line_end": section.get("line_end")}


def _model_id(name):
    return f"sldb://model/{name}"


def _document_id(document_id):
    return f"sldb://document/{document_id}"


def _section_id(section_id):
    return f"sldb://section/{section_id}"


def _semantic_tag_id(tag):
    return f"sldb://semantic_tag/{tag}"
