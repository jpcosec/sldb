---
id: python-sldb-sldb-store-edge_doc_contribution-_is_current
system: sldb
module: sldb.store.edge_doc_contribution
qualname: _is_current
kind: FunctionDef
source_path: sldb/store/edge_doc_contribution.py
source_span: '32:37'
source_sha256: d96d9dd3ee901bf13270c475186e4c27f4729c50a55ea60f753ef698c77ab28b
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_doc_contribution:_is_current; contract-sha256:d0c8ee02049943a2a4a1bd9b660fda343adaca8f23a35f2ea041e9ce97ba5760
---

# _is_current

## Signature

_is_current(cached: DocEdges, doc: DocumentEntry, contract: str)

## Docstring

`content_hash`, the tags and the model's contract are compared too: each can move without
the document's text (and so its `source_hash`) moving.

## Imports

["__future__", "sldb.store.edge_index.cache_keys", "sldb.store.edge_index.edge_rebuild_report", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.models", "typing"]

## Purpose

`content_hash`, the tags and the model's contract are compared too: each can move without the document's text (and so its `source_hash`) moving.

## Architecture

Not documented.
