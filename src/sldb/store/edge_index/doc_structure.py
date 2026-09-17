"""What a plain document contributes: its node, its sections, and the structural edges."""

from __future__ import annotations

from sldb.store.edge_index.node_ids import doc_node_id, model_node_id, section_node_id
from sldb.store.edge_index.records import edge, tagged_as
from sldb.store.models import DocumentEntry, EdgeContribution, EdgeNodeRecord, SectionContextRecord


def document_structure(model_name: str, doc: DocumentEntry, sections: list[SectionContextRecord]) -> EdgeContribution:
    """The document node (typed by its model), one node per section, and `has_document`,
    `has_section`, `tagged_as`."""
    export_id = f"{model_name}:{doc.name}"
    nodes = [_document_node(model_name, doc, export_id)] + [_section_node(export_id, s) for s in sections]
    edges = [edge(model_node_id(model_name), doc_node_id(export_id), "has_document", "structural")]
    edges += [edge(doc_node_id(export_id), section_node_id(export_id, s.path), "has_section", "structural") for s in sections]
    edges += tagged_as(doc_node_id(export_id), sorted(set(doc.semantic_tags)))
    for s in sections:
        edges += tagged_as(section_node_id(export_id, s.path), s.semantic_tags)
    return EdgeContribution(nodes=nodes, edges=edges)


def _document_node(model_name: str, doc: DocumentEntry, export_id: str) -> EdgeNodeRecord:
    semantics = {"export_id": export_id, "name": doc.name, "model": model_name, "path": doc.path, "semantic_tags": sorted(set(doc.semantic_tags)), "hash_c": doc.hash_c, "hash_d": doc.hash_d}
    return EdgeNodeRecord(id=doc_node_id(export_id), node_type=model_name, semantics=semantics)


def _section_node(export_id: str, section: SectionContextRecord) -> EdgeNodeRecord:
    semantics = {"export_id": f"{export_id}#{section.path}", "document_id": export_id, **section.model_dump()}
    return EdgeNodeRecord(id=section_node_id(export_id, section.path), node_type="sldb_section", semantics=semantics)
