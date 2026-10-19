---
id: python-sldb-sldb-api-graph-traverse-children
system: sldb
module: sldb.api.graph.traverse
qualname: children
kind: FunctionDef
source_path: sldb/api/graph/traverse.py
source_span: '36:38'
source_sha256: 6b7cc25ea0075260e80341c7fa94417aa45a1bf38d1df0eae119e50c73669ca6
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.traverse:children; contract-sha256:12b87087dcc852d0199dd99af30dfa0acb30e5bd8c2efae0a8ed7e35a8f7b5b7
---

# children

## Signature

children(store, node_id: str, relation: str, exclude_tags: Iterable[str]=())

## Docstring

The nodes pointing at `node_id` through `relation`.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.store.edge_index.node_ids", "sldb.store.graph", "typing"]

## Purpose

The nodes pointing at `node_id` through `relation`.

## Architecture

Not documented.
