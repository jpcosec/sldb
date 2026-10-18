---
id: python-sldb-sldb-store-section_sync-_sync_model_sections
system: sldb
module: sldb.store.section_sync
qualname: _sync_model_sections
kind: FunctionDef
source_path: sldb/store/section_sync.py
source_span: '41:53'
source_sha256: 7e586d1a7df88b4d407b8f0b5e5814800eb4e934bffe4a2d6a158da09d42220e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.section_sync:_sync_model_sections; contract-sha256:3a91d20cafefdb40e7f63b2314ce0dfd160b49547a3471317ed1e3100fd29f78
---

# _sync_model_sections

## Signature

_sync_model_sections(store_path, m_entry, m_idx, root, report, process_doc_sections)

## Docstring

PLAN 15 capa 8: `entries` is this operation's own cache (composed from shards at most
once); every document's file is still cheaply checked to exist (as before, for pruning
correctness), but only one in the dirty set (or every one, with no trustworthy baseline)
is actually opened and re-synced — an untouched document's sections shard is never read
just to confirm it agrees with a source_hash that has not moved.

## Imports

["__future__", "logging", "pathlib", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.section_doc_contribution", "sldb.store.section_paths"]

## Purpose

Not documented.

## Architecture

Not documented.
