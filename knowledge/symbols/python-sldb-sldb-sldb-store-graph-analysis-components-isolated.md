---
id: python-sldb-sldb-sldb-store-graph-analysis-components-isolated
system: sldb
module: sldb.sldb.store.graph.analysis.components
qualname: isolated
kind: FunctionDef
source_path: sldb/store/graph/analysis/components.py
source_span: '36:44'
source_sha256: 9fb4dae98b3da6125b3f9760f07a7fa15b12a301d9917c0cd8f76f1aa60a3421
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.graph.analysis.components:isolated;
  contract-sha256:a23c508049e87944137d04ac8b9d68cb4c664ff20bc71f4e9c8ac0ec5af4ded2
---

# isolated

## Signature

isolated(index, relations: object=None, node_types: object=None)

## Docstring

Nodes that no edge of the relations walked touches, of those classes if given.

Measured on the whole graph, then filtered: a node attached to something of another class is
not isolated.

## Imports

["__future__", "networkx", "sldb.store.graph.analysis.nx_graph", "sldb.store.graph.analysis.similarity"]

## Purpose

Not documented.

## Architecture

Not documented.
