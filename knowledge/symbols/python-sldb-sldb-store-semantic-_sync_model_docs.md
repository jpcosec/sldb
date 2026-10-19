---
id: python-sldb-sldb-store-semantic-_sync_model_docs
system: sldb
module: sldb.store.semantic
qualname: _sync_model_docs
kind: FunctionDef
source_path: sldb/store/semantic.py
source_span: 48:61
source_sha256: 2d75ff87dad55e74a774aebc76689fffb1c45b8a725db3179db76b763fd35215
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.semantic:_sync_model_docs; contract-sha256:625a9a3195860f2f998cbbef3bcd0d1f778ac859f5d125f3c3879bae107e2aaf
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
