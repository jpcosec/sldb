---
id: python-sldb-sldb-store-edge_index-doc_contribution-build_doc_edges
system: sldb
module: sldb.store.edge_index.doc_contribution
qualname: build_doc_edges
kind: FunctionDef
source_path: sldb/store/edge_index/doc_contribution.py
source_span: '16:38'
source_sha256: 2b167942c5eb3d35e4065601b06f477a96839ba8685bb4d0b6af2161d3889296
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.doc_contribution:build_doc_edges;
  contract-sha256:e2e8d5317107a11c5d56b24b14ce3b80a9873772ececfa80a354333f8cae8b99
---

# build_doc_edges

## Signature

build_doc_edges(model_name: str, doc: DocumentEntry, sections: list[SectionContextRecord], payload_of: Callable[[], dict[str, Any] | None], model_type: Any | None=None)

## Docstring

A relation type, relation or anchor document contributes what it declares; any other
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

## Imports

["__future__", "sldb.store.edge_index.composition_edges", "sldb.store.edge_index.declared_references", "sldb.store.edge_index.doc_kinds", "sldb.store.edge_index.doc_structure", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.records", "sldb.store.models", "typing"]

## Purpose

A relation type, relation or anchor document contributes what it declares; any other document contributes itself, its sections, and the references its model declares. Either way its tags become nodes: a tag exists in the index because some document, model or DAG entry carries it.

## Architecture

Not documented.
