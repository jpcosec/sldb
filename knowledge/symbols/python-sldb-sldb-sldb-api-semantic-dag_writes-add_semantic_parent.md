---
id: python-sldb-sldb-sldb-api-semantic-dag_writes-add_semantic_parent
system: sldb
module: sldb.sldb.api.semantic.dag_writes
qualname: add_semantic_parent
kind: FunctionDef
source_path: sldb/api/semantic/dag_writes.py
source_span: '20:27'
source_sha256: 88d3bee0a6e179f78e4d7d06153cedf2c3862443897c28fc61af62ed56c50e74
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.semantic.dag_writes:add_semantic_parent;
  contract-sha256:ec2cbfe2e31487f9430c1a96b659c4a331843700e408d90cfffdafccb5e89ada
---

# add_semantic_parent

## Signature

add_semantic_parent(store: str | Path | None, tag: str, parent: str, actor: str | None=None)

## Docstring

Declare `tag` a kind of `parent`. True when the DAG changed, False when it already said so.

Raises:
    SLDBStoreError: When either tag is unknown, or the edge would close a cycle.

## Imports

["__future__", "pathlib", "sldb.api.journal", "sldb.api.stores.open_store", "sldb.store", "sldb.store.edge_rebuild", "sldb.store.io"]

## Purpose

Not documented.

## Architecture

Not documented.
