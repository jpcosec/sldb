---
id: python-sldb-sldb-sldb-store-edge_index-composition_edges-composition_edges
system: sldb
module: sldb.sldb.store.edge_index.composition_edges
qualname: composition_edges
kind: FunctionDef
source_path: sldb/store/edge_index/composition_edges.py
source_span: '28:42'
source_sha256: f01b85254d77f3aa8cde82d837c90b6c71fcdc3fdd7ebdd4ffdfff6ae61a51b9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_index.composition_edges:composition_edges;
  contract-sha256:91a0d85800bbff63391c56ce5a99c0eb654e478466fe808a59b2836f610bcacf
---

# composition_edges

## Signature

composition_edges(source: str, model_type: Any | None, payload: Payload | None)

## Docstring

One edge per ref held by a composed field's source field, in declaration order.

Args:
    source: Node id of the composing document.
    model_type: The imported model class, or None when it cannot be imported.
    payload: The document's extracted payload, or None when it cannot be read.

Returns:
    `composes` edges whose target is still a path, to be resolved at compose time.

## Imports

["__future__", "sldb.store.models", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
