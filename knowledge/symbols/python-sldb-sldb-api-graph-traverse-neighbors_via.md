---
id: python-sldb-sldb-api-graph-traverse-neighbors_via
system: sldb
module: sldb.api.graph.traverse
qualname: neighbors_via
kind: FunctionDef
source_path: sldb/api/graph/traverse.py
source_span: '52:57'
source_sha256: 6b7cc25ea0075260e80341c7fa94417aa45a1bf38d1df0eae119e50c73669ca6
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.graph.traverse:neighbors_via; contract-sha256:2cba8666ac690fd816bc4adab340d461b9b2aebd3ece05ff43218a73ee24eeb8
---

# neighbors_via

## Signature

neighbors_via(store, node_id: str, out_relation: str, in_relation: str | None=None, exclude_prefixes: tuple[str, ...]=(), same_kind: bool=True, exclude_tags: Iterable[str]=())

## Docstring

The nodes sharing an `out_relation` target with `node_id`, same kind by default.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.store.edge_index.node_ids", "sldb.store.graph", "typing"]

## Purpose

The nodes sharing an `out_relation` target with `node_id`, same kind by default.

## Architecture

Not documented.
