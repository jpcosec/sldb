---
id: python-sldb-sldb-store-graph-analysis-centrality-central
system: sldb
module: sldb.store.graph.analysis.centrality
qualname: central
kind: FunctionDef
source_path: sldb/store/graph/analysis/centrality.py
source_span: '27:36'
source_sha256: 303755778339ea44056fb2a6e3a4ee72dc173ec4784c4af508830a532e06b531
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.centrality:central; contract-sha256:9b1624d1163fbe6db0461ba0f57d0db06c515ad4ea367489093ed0ec9e186405
---

# central

## Signature

central(index, kind: str='pagerank', relations: object=None, node_types: object=None, limit: int=20)

## Docstring

The `limit` most central nodes with their score, highest first.

`kind` is one of `KINDS`. Ties break by node id so the answer is stable.

## Imports

["__future__", "networkx", "sldb.store.exceptions", "sldb.store.graph.analysis.nx_graph", "sldb.store.graph.analysis.similarity"]

## Purpose

The `limit` most central nodes with their score, highest first.

## Architecture

Not documented.
