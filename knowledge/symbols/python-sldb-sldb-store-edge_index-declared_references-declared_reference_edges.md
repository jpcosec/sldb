---
id: python-sldb-sldb-store-edge_index-declared_references-declared_reference_edges
system: sldb
module: sldb.store.edge_index.declared_references
qualname: declared_reference_edges
kind: FunctionDef
source_path: sldb/store/edge_index/declared_references.py
source_span: 38:61
source_sha256: 3135fa4da4e7b18edad0f0514e5a2531587954b72435c148d98245aac35e6cda
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.declared_references:declared_reference_edges;
  contract-sha256:00e6e1b8d03910c4d16738e931a4883dc1cb7b07559e47360617ad55e9c70213
---

# declared_reference_edges

## Signature

declared_reference_edges(model_name: str, doc_name: str, model_type: Any | None, payload: Payload | None)

## Docstring

The edges the model's `__references__` and `__containment__` declare for this document.

Args:
    model_name: Model the document is tracked under.
    doc_name: The document's name, used for its own node id.
    model_type: The imported model class, or None when it cannot be imported (a linked
        store's model): nothing is declared then, as in `build_model_edges`.
    payload: The document's extracted payload, or None when it cannot be read.

Returns:
    One edge per id found, `contains` for containment fields and `references` for the
    rest. Order follows the declaration, then the order of ids inside each field.

## Imports

["__future__", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.records", "sldb.store.models", "typing"]

## Purpose

The edges the model's `__references__` and `__containment__` declare for this document.

## Architecture

Not documented.
