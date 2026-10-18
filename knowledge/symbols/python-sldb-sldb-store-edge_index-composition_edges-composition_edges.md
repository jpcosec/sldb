---
id: python-sldb-sldb-store-edge_index-composition_edges-composition_edges
system: sldb
module: sldb.store.edge_index.composition_edges
qualname: composition_edges
kind: FunctionDef
source_path: sldb/store/edge_index/composition_edges.py
source_span: '28:42'
source_sha256: f01b85254d77f3aa8cde82d837c90b6c71fcdc3fdd7ebdd4ffdfff6ae61a51b9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.composition_edges:composition_edges;
  contract-sha256:00bda7d0a065fab180833844e1222c8b7d80da0268ce6017f923278d9a94065c
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
