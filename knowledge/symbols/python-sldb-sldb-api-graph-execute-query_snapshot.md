---
id: python-sldb-sldb-api-graph-execute-query_snapshot
system: sldb
module: sldb.api.graph.execute
qualname: query_snapshot
kind: FunctionDef
source_path: sldb/api/graph/execute.py
source_span: '32:37'
source_sha256: fae0dafbb9772dee4b9cee631d45bac6fe7aac7030edd6e8896ed8333c8332fa
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.graph.execute:query_snapshot; contract-sha256:746e73e2afe000703095ed98783e3347e1e7458804be406588a85e2f52b29b99
---

# query_snapshot

## Signature

query_snapshot(snapshot, query: StructuredQuery)

## Docstring

Execute a StructuredQuery over a GraphSnapshot held in memory (e.g. from `snapshot_load`),
no store needed; the same matching as `execute_query`.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.store.graph.executor", "sldb.store.graph.language", "sldb.store.graph.node_view", "typing"]

## Purpose

Execute a StructuredQuery over a GraphSnapshot held in memory (e.g. from `snapshot_load`), no store needed; the same matching as `execute_query`.

## Architecture

Not documented.
