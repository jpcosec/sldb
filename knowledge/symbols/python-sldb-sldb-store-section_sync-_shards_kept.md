---
id: python-sldb-sldb-store-section_sync-_shards_kept
system: sldb
module: sldb.store.section_sync
qualname: _shards_kept
kind: FunctionDef
source_path: sldb/store/section_sync.py
source_span: 72:76
source_sha256: 34a5d402dcd44758faba73ddc8862f6ceac89270c742a4e46f87f99ae956794d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.section_sync:_shards_kept; contract-sha256:ba39f6184652e44807e71702e2fb484eec9129d6ff760cf5c53e28f5a4c11ddb
---

# _shards_kept

## Signature

_shards_kept(shards_dir: Path, m_idx)

## Docstring

The user cache says the shards are current; they are only if they are still there. A
deleted `.sldb/runtime/` left the cache trusting shards that no longer existed, so no
rebuild (nor `stores update`) brought sections back.

## Imports

["__future__", "logging", "pathlib", "sldb.store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.layout", "sldb.store.section_doc_contribution", "sldb.store.section_paths"]

## Purpose

The user cache says the shards are current; they are only if they are still there. A deleted `.sldb/runtime/` left the cache trusting shards that no longer existed, so no rebuild (nor `stores update`) brought sections back.

## Architecture

Not documented.
