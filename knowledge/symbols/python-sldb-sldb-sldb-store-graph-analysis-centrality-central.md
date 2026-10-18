---
id: python-sldb-sldb-sldb-store-graph-analysis-centrality-central
system: sldb
module: sldb.sldb.store.graph.analysis.centrality
qualname: central
kind: FunctionDef
source_path: sldb/store/graph/analysis/centrality.py
source_span: '27:36'
source_sha256: 303755778339ea44056fb2a6e3a4ee72dc173ec4784c4af508830a532e06b531
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.graph.analysis.centrality:central; contract-sha256:4ec3ce361b76e2ea082a799cacf341878768a24bf33ae0bf4347f280600705a6
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

Not documented.

## Architecture

Not documented.
