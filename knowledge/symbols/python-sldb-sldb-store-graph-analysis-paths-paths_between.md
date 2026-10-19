---
id: python-sldb-sldb-store-graph-analysis-paths-paths_between
system: sldb
module: sldb.store.graph.analysis.paths
qualname: paths_between
kind: FunctionDef
source_path: sldb/store/graph/analysis/paths.py
source_span: '24:30'
source_sha256: 7a7bda6a25c639e520767c07ad12c8bba467fb2b59c0708ac62dcbaddbda6fd0
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.paths:paths_between; contract-sha256:477165e11dd8dc2e4e94682f1d2cecb7a16b8a7b5fda0489119cd57fce8923bd
---

# paths_between

## Signature

paths_between(index, source: str, target: str, relations: object=None, cutoff: int | None=None, limit: int=10)

## Docstring

Up to `limit` distinct chains between the two nodes, shortest first, at most `cutoff` hops.

## Imports

["__future__", "networkx", "sldb.store.graph.analysis.nx_graph"]

## Purpose

Up to `limit` distinct chains between the two nodes, shortest first, at most `cutoff` hops.

## Architecture

Not documented.
