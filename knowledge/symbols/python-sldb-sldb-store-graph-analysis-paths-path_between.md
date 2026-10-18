---
id: python-sldb-sldb-store-graph-analysis-paths-path_between
system: sldb
module: sldb.store.graph.analysis.paths
qualname: path_between
kind: FunctionDef
source_path: sldb/store/graph/analysis/paths.py
source_span: '10:21'
source_sha256: 7a7bda6a25c639e520767c07ad12c8bba467fb2b59c0708ac62dcbaddbda6fd0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.graph.analysis.paths:path_between; contract-sha256:1f2be78357ed6921220203b8771360fa7e7c439cc4989352d6e8ba1a17101a7c
---

# path_between

## Signature

path_between(index, source: str, target: str, relations: object=None, directed: bool=False)

## Docstring

The shortest chain of nodes from `source` to `target`, or None when there is none.

Undirected by default: `a implements b` connects the two whichever end you start from.

## Imports

["__future__", "networkx", "sldb.store.graph.analysis.nx_graph"]

## Purpose

The shortest chain of nodes from `source` to `target`, or None when there is none.

## Architecture

Not documented.
