---
id: python-sldb-sldb-store-graph-analysis-cycles-cycles
system: sldb
module: sldb.store.graph.analysis.cycles
qualname: cycles
kind: FunctionDef
source_path: sldb/store/graph/analysis/cycles.py
source_span: '15:18'
source_sha256: a7d9df683f72c14e1f7452fc0e9623d64e9906618ef3b72dc9fc631430ca39e3
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.cycles:cycles; contract-sha256:e3cea7d836c1dfbfed0abc5b3dcae9ecdf73c92bc001259755b6f3c4216e152d
---

# cycles

## Signature

cycles(index, relations: object=None, limit: int=10)

## Docstring

Up to `limit` cycles in the relations walked, shortest first; empty when it is a DAG.

## Imports

["__future__", "networkx", "sldb.store.graph.analysis.nx_graph"]

## Purpose

Up to `limit` cycles in the relations walked, shortest first; empty when it is a DAG.

## Architecture

Not documented.
