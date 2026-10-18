---
id: python-sldb-sldb-sldb-store-io-_save_if_changed
system: sldb
module: sldb.sldb.store.io
qualname: _save_if_changed
kind: FunctionDef
source_path: sldb/store/io/__init__.py
source_span: 67:76
source_sha256: a65d487517f80e48a31662a55b977d5d2a86eaaa5f6dc2379c796c8b06ddfee0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.io:_save_if_changed; contract-sha256:4a9c91412a422391b3cb5acd21af4a2ea77be49fc02817016fc12a2a810d1049
---

# _save_if_changed

## Signature

_save_if_changed(path: Path, index, saver)

## Docstring

Write only when the content differs from what the file already holds: a rebuild that
changes nothing leaves the file, its mtime and every cache keyed on it alone.

## Imports

["pathlib", "sldb.store.io.documents_index", "sldb.store.io.lock", "sldb.store.io.models_index", "sldb.store.io.sections_index", "sldb.store.io.semantic_dag", "sldb.store.io.semantic_index", "sldb.store.io.store_index", "sldb.store.layout", "sldb.store.models"]

## Purpose

Not documented.

## Architecture

Not documented.
