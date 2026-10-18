---
id: python-sldb-sldb-store-graph-analysis-order-topological_order
system: sldb
module: sldb.store.graph.analysis.order
qualname: topological_order
kind: FunctionDef
source_path: sldb/store/graph/analysis/order.py
source_span: '12:20'
source_sha256: d33e90091b97e86dc4e2017ab53967ca208e0fa78b44a037a8c5ccd3e96c4e20
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.order:topological_order; contract-sha256:cb603e5b3d0a1f7f1f5ff572f0b53c52c319dae9944266a05dd686a2d8401d2c
---

# topological_order

## Signature

topological_order(index, relations: object=None)

## Docstring

Every node ordered so a node comes after everything it points at.

Raises `SLDBGraphCycleError` with the offending cycle when the relation is not a DAG.

## Imports

["__future__", "networkx", "sldb.store.exceptions", "sldb.store.graph.analysis.cycles", "sldb.store.graph.analysis.nx_graph"]

## Purpose

Not documented.

## Architecture

Not documented.
