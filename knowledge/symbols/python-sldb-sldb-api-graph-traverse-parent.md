---
id: python-sldb-sldb-api-graph-traverse-parent
system: sldb
module: sldb.api.graph.traverse
qualname: parent
kind: FunctionDef
source_path: sldb/api/graph/traverse.py
source_span: '41:43'
source_sha256: 6b7cc25ea0075260e80341c7fa94417aa45a1bf38d1df0eae119e50c73669ca6
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.traverse:parent; contract-sha256:13fc17c67cdc4ccf845d69d5c170c8574fb95e5c5cc2e247ac3a6ed132efae92
---

# parent

## Signature

parent(store, node_id: str, relation: str, exclude_tags: Iterable[str]=())

## Docstring

The first node `node_id` points at through `relation`, or None.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.store.edge_index.node_ids", "sldb.store.graph", "typing"]

## Purpose

The first node `node_id` points at through `relation`, or None.

## Architecture

Not documented.
