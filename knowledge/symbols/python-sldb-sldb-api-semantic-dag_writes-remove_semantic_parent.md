---
id: python-sldb-sldb-api-semantic-dag_writes-remove_semantic_parent
system: sldb
module: sldb.api.semantic.dag_writes
qualname: remove_semantic_parent
kind: FunctionDef
source_path: sldb/api/semantic/dag_writes.py
source_span: '30:37'
source_sha256: 88d3bee0a6e179f78e4d7d06153cedf2c3862443897c28fc61af62ed56c50e74
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.semantic.dag_writes:remove_semantic_parent;
  contract-sha256:a94f357e886d3360059b853a464f39442f202da34b24884a6ec3195e07221b0e
---

# remove_semantic_parent

## Signature

remove_semantic_parent(store: str | Path | None, tag: str, parent: str, actor: str | None=None)

## Docstring

Undeclare it. True when the DAG changed.

Raises:
    SLDBStoreError: When the parent is the one the tag's own name implies.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.stores.open_store", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
