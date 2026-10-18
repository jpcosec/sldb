---
id: python-sldb-sldb-sldb-api-semantic-dag_writes-add_semantic_equivalence
system: sldb
module: sldb.sldb.api.semantic.dag_writes
qualname: add_semantic_equivalence
kind: FunctionDef
source_path: sldb/api/semantic/dag_writes.py
source_span: '40:44'
source_sha256: 88d3bee0a6e179f78e4d7d06153cedf2c3862443897c28fc61af62ed56c50e74
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.semantic.dag_writes:add_semantic_equivalence;
  contract-sha256:38cb460483202eb1541c4430db45218c1d7d0f6f424ee5d9f1786c6bae144d4f
---

# add_semantic_equivalence

## Signature

add_semantic_equivalence(store: str | Path | None, local_tag: str, global_tag: str, actor: str | None=None)

## Docstring

Map a local tag to a global one, for `gse.` across linked stores. True when the DAG
changed. The store function this wraps existed for a long time with no caller at all.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.stores.open_store", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
