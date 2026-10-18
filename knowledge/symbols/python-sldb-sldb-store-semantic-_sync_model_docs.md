---
id: python-sldb-sldb-store-semantic-_sync_model_docs
system: sldb
module: sldb.store.semantic
qualname: _sync_model_docs
kind: FunctionDef
source_path: sldb/store/semantic.py
source_span: 48:61
source_sha256: 51c6b9afc86175d457240d8d9da3b5a7591c9439bc7f46489db64c49a1b4cee3
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.semantic:_sync_model_docs; contract-sha256:36948bff17eeb1b9424c5af258544459e73258f4ca43dc351af993ff54214eb3
---

# _sync_model_docs

## Signature

_sync_model_docs(store_path, m_entry, m_idx, root, resolver, py_path, report, new_tags: set)

## Docstring

PLAN 15 capa 7: a document's own shard (path, source_hash, content_hash, semantic_tags) is
rewritten only when its semantic_tags actually changed by this sync — not the whole
model's documents index, and not every document's shard just because one changed. PLAN
15 capa 8: with a trustworthy dirty set (this operation's own writes, or a prior sync's
clean baseline), only those documents are even opened — an untouched one's semantic
shard is never read just to confirm it agrees with a source_hash that has not moved.

## Imports

["__future__", "dataclasses", "pathlib", "re", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.semantic_dag_sync", "sldb.store.semantic_doc_contribution"]

## Purpose

PLAN 15 capa 7: a document's own shard (path, source_hash, content_hash, semantic_tags) is rewritten only when its semantic_tags actually changed by this sync — not the whole model's documents index, and not every document's shard just because one changed. PLAN 15 capa 8: with a trustworthy dirty set (this operation's own writes, or a prior sync's clean baseline), only those documents are even opened — an untouched one's semantic shard is never read just to confirm it agrees with a source_hash that has not moved.

## Architecture

Not documented.
