---
id: python-sldb-sldb-sldb-store-graph-analysis-paths-path_between
system: sldb
module: sldb.sldb.store.graph.analysis.paths
qualname: path_between
kind: FunctionDef
source_path: sldb/store/graph/analysis/paths.py
source_span: '10:21'
source_sha256: 7a7bda6a25c639e520767c07ad12c8bba467fb2b59c0708ac62dcbaddbda6fd0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.graph.analysis.paths:path_between; contract-sha256:9eab13510c5d341d6fcd308d69545e0ea5cc0043fcdc82d35ce6926f53209e24
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

Not documented.

## Architecture

Not documented.
