---
id: python-sldb-sldb-sldb-store-semantic-_sync_model
system: sldb
module: sldb.sldb.store.semantic
qualname: _sync_model
kind: FunctionDef
source_path: sldb/store/semantic.py
source_span: '34:45'
source_sha256: 51c6b9afc86175d457240d8d9da3b5a7591c9439bc7f46489db64c49a1b4cee3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.semantic:_sync_model; contract-sha256:df9d804328555dcede79b0aac286072ac7c88beb65286ba048d102f8e04111da
---

# _sync_model

## Signature

_sync_model(store_path, m_entry, root, resolver, py_path, report, new_tags: set)

## Docstring

Every document's semantic shard brought current; skipped whole when the model's
roster_hash (covering every one of its documents) has not moved since the last sync — no
shard is even opened (PLAN 15 capa 5).

## Imports

["__future__", "dataclasses", "pathlib", "re", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.semantic_dag_sync", "sldb.store.semantic_doc_contribution"]

## Purpose

Not documented.

## Architecture

Not documented.
