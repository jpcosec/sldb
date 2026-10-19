---
id: python-sldb-sldb-api-edges-edge_reading-edge_node
system: sldb
module: sldb.api.edges.edge_reading
qualname: edge_node
kind: FunctionDef
source_path: sldb/api/edges/edge_reading.py
source_span: '52:54'
source_sha256: 843bafb03f66570ae4a91c980e7c72edc694998e17af5edc4882a34b62ba45b5
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.edges.edge_reading:edge_node; contract-sha256:a7502cedd14f25fd0cda04afecfdab6bc41d7881e2efda0a9bbdd188937a89c7
---

# edge_node

## Signature

edge_node(store: str | Path | None, node_id: str, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

The node with that node id (or document export id); None when the index has none.

## Imports

["__future__", "pathlib", "sldb.api.stores.open_store", "sldb.store.edge_index.compose", "sldb.store.edge_index.edge_index", "sldb.store.models", "typing"]

## Purpose

The node with that node id (or document export id); None when the index has none.

## Architecture

Not documented.
