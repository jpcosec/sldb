---
id: python-sldb-sldb-store-semantic-_sync_model
system: sldb
module: sldb.store.semantic
qualname: _sync_model
kind: FunctionDef
source_path: sldb/store/semantic.py
source_span: '34:45'
source_sha256: 2d75ff87dad55e74a774aebc76689fffb1c45b8a725db3179db76b763fd35215
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.semantic:_sync_model; contract-sha256:263f645993923d38a51d333cdc7ae313d4941b0228f819b762cfb399c7bc4bc7
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

Every document's semantic shard brought current; skipped whole when the model's roster_hash (covering every one of its documents) has not moved since the last sync — no shard is even opened (PLAN 15 capa 5).

## Architecture

Not documented.
