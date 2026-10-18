---
id: python-sldb-sldb-store-journal-verify-verify_chain
system: sldb
module: sldb.store.journal.verify
qualname: verify_chain
kind: FunctionDef
source_path: sldb/store/journal/verify.py
source_span: '14:24'
source_sha256: a78496ac4cbea1a654aab10e4f1a0c0d679f8239f1d73923452aa8b2eb98d76d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.journal.verify:verify_chain; contract-sha256:10139d89c84a93ca79f4df11ce7aa422d17fe665274d2890407359bb9fac93c3
---

# verify_chain

## Signature

verify_chain(store_path: Path)

## Docstring

Walk the journal oldest-first, checking each entry's hash and link to the previous.

## Imports

["__future__", "pathlib", "sldb.store.io.utils", "sldb.store.journal.entry", "sldb.store.journal.hashing", "sldb.store.journal.layout", "sldb.store.journal.report"]

## Purpose

Walk the journal oldest-first, checking each entry's hash and link to the previous.

## Architecture

Not documented.
