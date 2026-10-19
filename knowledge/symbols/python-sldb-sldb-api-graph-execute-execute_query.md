---
id: python-sldb-sldb-api-graph-execute-execute_query
system: sldb
module: sldb.api.graph.execute
qualname: execute_query
kind: FunctionDef
source_path: sldb/api/graph/execute.py
source_span: '13:15'
source_sha256: fae0dafbb9772dee4b9cee631d45bac6fe7aac7030edd6e8896ed8333c8332fa
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.execute:execute_query; contract-sha256:41f50933e5e012593c08a9471d86b2f9c102503027fe1e366ee8b54dee238e90
---

# execute_query

## Signature

execute_query(store, query: StructuredQuery, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

Execute a StructuredQuery over the store's edge index; returns matching nodes.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.store.graph.executor", "sldb.store.graph.language", "sldb.store.graph.node_view", "typing"]

## Purpose

Execute a StructuredQuery over the store's edge index; returns matching nodes.

## Architecture

Not documented.
