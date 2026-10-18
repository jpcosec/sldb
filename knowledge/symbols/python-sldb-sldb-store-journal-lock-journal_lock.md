---
id: python-sldb-sldb-store-journal-lock-journal_lock
system: sldb
module: sldb.store.journal.lock
qualname: journal_lock
kind: FunctionDef
source_path: sldb/store/journal/lock.py
source_span: '14:24'
source_sha256: ad5d2191392e33e03a16dea690738e60dff21c27bc8e7b97d37159d019b0f846
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.journal.lock:journal_lock; contract-sha256:f4a6dc04769b76769e675382c39c43d0fa58b35db2728d4e4ca05304c3b7cd95
---

# journal_lock

## Signature

journal_lock(store_path: Path)

## Docstring

Hold the journal lock while the caller appends, so the chain never interleaves.

## Imports

["__future__", "contextlib", "fcntl", "os", "pathlib", "sldb.store.journal.layout"]

## Purpose

Hold the journal lock while the caller appends, so the chain never interleaves.

## Architecture

Not documented.
