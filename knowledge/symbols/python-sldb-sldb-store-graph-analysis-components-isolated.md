---
id: python-sldb-sldb-store-graph-analysis-components-isolated
system: sldb
module: sldb.store.graph.analysis.components
qualname: isolated
kind: FunctionDef
source_path: sldb/store/graph/analysis/components.py
source_span: '36:44'
source_sha256: 9fb4dae98b3da6125b3f9760f07a7fa15b12a301d9917c0cd8f76f1aa60a3421
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.components:isolated; contract-sha256:25727b59e8706f8f32cfd0b5a9607eac3ab93183ff80930253a3d9e6a7b23811
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

Nodes that no edge of the relations walked touches, of those classes if given.

## Architecture

Not documented.
