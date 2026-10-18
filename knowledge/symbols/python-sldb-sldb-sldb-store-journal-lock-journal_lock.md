---
id: python-sldb-sldb-sldb-store-journal-lock-journal_lock
system: sldb
module: sldb.sldb.store.journal.lock
qualname: journal_lock
kind: FunctionDef
source_path: sldb/store/journal/lock.py
source_span: '14:24'
source_sha256: ad5d2191392e33e03a16dea690738e60dff21c27bc8e7b97d37159d019b0f846
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.journal.lock:journal_lock; contract-sha256:6be8483dbe0ec2e0d0f9571d6f0a1888d3fab2d41c7cfc69963c1ac8bd4fc000
---

# journal_lock

## Signature

journal_lock(store_path: Path)

## Docstring

Hold the journal lock while the caller appends, so the chain never interleaves.

## Imports

["__future__", "contextlib", "fcntl", "os", "pathlib", "sldb.store.journal.layout"]

## Purpose

Not documented.

## Architecture

Not documented.
