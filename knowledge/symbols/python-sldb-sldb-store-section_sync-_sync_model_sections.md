---
id: python-sldb-sldb-store-section_sync-_sync_model_sections
system: sldb
module: sldb.store.section_sync
qualname: _sync_model_sections
kind: FunctionDef
source_path: sldb/store/section_sync.py
source_span: '41:53'
source_sha256: 34a5d402dcd44758faba73ddc8862f6ceac89270c742a4e46f87f99ae956794d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.section_sync:_sync_model_sections; contract-sha256:1857b562fc4bc279845340b95d2ec2dd818729f640d673b3c36b84106c7497c9
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

PLAN 15 capa 8: `entries` is this operation's own cache (composed from shards at most once); every document's file is still cheaply checked to exist (as before, for pruning correctness), but only one in the dirty set (or every one, with no trustworthy baseline) is actually opened and re-synced — an untouched document's sections shard is never read just to confirm it agrees with a source_hash that has not moved.

## Architecture

Not documented.
