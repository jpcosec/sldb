---
id: python-sldb-sldb-api-graph-analyze-graph_paths
system: sldb
module: sldb.api.graph.analyze
qualname: graph_paths
kind: FunctionDef
source_path: sldb/api/graph/analyze.py
source_span: '22:24'
source_sha256: 514fb5d5270290f5668091039e4310a917f116a12720f780712ce3221e0a96c1
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.analyze:graph_paths; contract-sha256:bb8efa6721cf6b65055c8a37d9ba597cd7e4404286a209d40c6749d3e74a1dcc
---

# graph_paths

## Signature

graph_paths(store, source: str, target: str, relations: object=None, cutoff: int | None=None, limit: int=10, **index)

## Docstring

Up to `limit` distinct chains between two nodes, shortest first.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.core.exceptions", "sldb.store.graph", "typing"]

## Purpose

Up to `limit` distinct chains between two nodes, shortest first.

## Architecture

Not documented.
