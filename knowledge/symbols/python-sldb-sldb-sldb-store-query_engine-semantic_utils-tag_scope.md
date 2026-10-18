---
id: python-sldb-sldb-sldb-store-query_engine-semantic_utils-tag_scope
system: sldb
module: sldb.sldb.store.query_engine.semantic_utils
qualname: tag_scope
kind: FunctionDef
source_path: sldb/store/query_engine/semantic_utils.py
source_span: '26:33'
source_sha256: 4ad80c6c32c0718ef773607f8cbe6c5f96854ffe8004dc8bb8c5557271582761
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.query_engine.semantic_utils:tag_scope;
  contract-sha256:2012bb3826369823d0a56c9d7165fb02a436ef86f53becd63df693e75ad34196
---

# tag_scope

## Signature

tag_scope(store_path: Path, tag: str)

## Docstring

The tag and every tag under it in the store's DAG: what naming it reaches.

Naming a parent used to reach nothing: `se.type.knowledge` answered `[]` while 29 documents
hung under it, because a document is tagged with the leaf and the edges to the parent had no
reader. Reading them is the whole point of the DAG being a graph.

## Imports

["__future__", "pathlib", "re", "sldb.store.io", "sldb.store.layout", "sldb.store.query", "sldb.store.query_engine.models", "sldb.store.semantic_dag_graph", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
