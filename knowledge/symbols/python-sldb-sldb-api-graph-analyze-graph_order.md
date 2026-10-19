---
id: python-sldb-sldb-api-graph-analyze-graph_order
system: sldb
module: sldb.api.graph.analyze
qualname: graph_order
kind: FunctionDef
source_path: sldb/api/graph/analyze.py
source_span: '32:34'
source_sha256: 514fb5d5270290f5668091039e4310a917f116a12720f780712ce3221e0a96c1
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.analyze:graph_order; contract-sha256:5a9db466a04fa169df5ed53175edbf8f3d9138ce6b91606ea9fdf9862595ef6a
---

# graph_order

## Signature

graph_order(store, relations: object=None, **index)

## Docstring

Every node in dependency order; raises `SLDBGraphCycleError` when not a DAG.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.core.exceptions", "sldb.store.graph", "typing"]

## Purpose

Every node in dependency order; raises `SLDBGraphCycleError` when not a DAG.

## Architecture

Not documented.
