---
id: python-sldb-sldb-store-semantic_dag_graph-relative
system: sldb
module: sldb.store.semantic_dag_graph
qualname: relative
kind: FunctionDef
source_path: sldb/store/semantic_dag_graph.py
source_span: 61:64
source_sha256: 134d81e7ebc669c69f7a36d02140b55c41c04bf3c28811d3d8198b93a24149bb
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.semantic_dag_graph:relative; contract-sha256:6ce59e2b848f661e3df44317e69ded9dacce090bd5b4503e2a6118518a33a273
---

# relative

## Signature

relative(tag: str, prefix: str)

## Docstring

How a child reads under its parent: the trailing segment, or the whole id when it is not
a prefix of the child — which is what a parent declared by hand looks like.

## Imports

["__future__", "networkx"]

## Purpose

How a child reads under its parent: the trailing segment, or the whole id when it is not a prefix of the child — which is what a parent declared by hand looks like.

## Architecture

Not documented.
