---
id: python-sldb-sldb-api-graph-execute-graph_get
system: sldb
module: sldb.api.graph.execute
qualname: graph_get
kind: FunctionDef
source_path: sldb/api/graph/execute.py
source_span: '18:24'
source_sha256: fae0dafbb9772dee4b9cee631d45bac6fe7aac7030edd6e8896ed8333c8332fa
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.execute:graph_get; contract-sha256:8c245e4d1209702f934a748d91afca8c3ced1793a2ec732139d5198101bdd496
---

# graph_get

## Signature

graph_get(store, node_id: str, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

One node by id, with its edges; None when the index has no such node.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.store.graph.executor", "sldb.store.graph.language", "sldb.store.graph.node_view", "typing"]

## Purpose

One node by id, with its edges; None when the index has no such node.

## Architecture

Not documented.
