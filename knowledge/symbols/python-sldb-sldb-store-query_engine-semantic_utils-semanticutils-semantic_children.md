---
id: python-sldb-sldb-store-query_engine-semantic_utils-semanticutils-semantic_children
system: sldb
module: sldb.store.query_engine.semantic_utils
qualname: SemanticUtils.semantic_children
kind: FunctionDef
source_path: sldb/store/query_engine/semantic_utils.py
source_span: 55:64
source_sha256: 4ad80c6c32c0718ef773607f8cbe6c5f96854ffe8004dc8bb8c5557271582761
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.query_engine.semantic_utils:SemanticUtils.semantic_children;
  contract-sha256:c63c07d29fc86976c02a62a6db0cb92afa50065a8525f01a9312baad802c9d10
---

# SemanticUtils.semantic_children

## Signature

semantic_children(cls, store_path: Path, prefix: str)

## Docstring

Child semantic nodes, read off the DAG's edges rather than matched as strings.

`se` lists the tags with no parent; `se.<tag>` lists the tags that declare it as one.
A child whose name is not the parent's name plus a segment comes back whole: that is
what a parent declared by hand, instead of derived from the dotted name, looks like.

## Imports

["__future__", "pathlib", "re", "sldb.store.io", "sldb.store.layout", "sldb.store.query", "sldb.store.query_engine.models", "sldb.store.semantic_dag_graph", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
