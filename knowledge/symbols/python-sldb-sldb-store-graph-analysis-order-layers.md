---
id: python-sldb-sldb-store-graph-analysis-order-layers
system: sldb
module: sldb.store.graph.analysis.order
qualname: layers
kind: FunctionDef
source_path: sldb/store/graph/analysis/order.py
source_span: '23:28'
source_sha256: d33e90091b97e86dc4e2017ab53967ca208e0fa78b44a037a8c5ccd3e96c4e20
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.order:layers; contract-sha256:ef99c7efa9ee6a4c2eb8c5cae0941e3db8a2d5c89c25389dd1193a82b1065425
---

# layers

## Signature

layers(index, relations: object=None)

## Docstring

The same order as levels: everything in a level depends only on earlier levels.

## Imports

["__future__", "networkx", "sldb.store.exceptions", "sldb.store.graph.analysis.cycles", "sldb.store.graph.analysis.nx_graph"]

## Purpose

The same order as levels: everything in a level depends only on earlier levels.

## Architecture

Not documented.
