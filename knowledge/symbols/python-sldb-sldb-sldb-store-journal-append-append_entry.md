---
id: python-sldb-sldb-sldb-store-journal-append-append_entry
system: sldb
module: sldb.sldb.store.journal.append
qualname: append_entry
kind: FunctionDef
source_path: sldb/store/journal/append.py
source_span: '23:28'
source_sha256: 3bc2322e5dde4795c66c7339c0d7f2f9bf4bc49ba99fb54f7344ec742d3991a9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.journal.append:append_entry; contract-sha256:2579c70345ea677f266134398e2d49dd7f1078fb230b3b6781f5287e1ca796a1
---

# append_entry

## Signature

append_entry(store_path: Path, data: dict[str, Any])

## Docstring

Record one write, chained to the journal's previous entry, under the journal lock.

## Imports

["__future__", "os", "pathlib", "sldb.store.io.utils", "sldb.store.journal.entry", "sldb.store.journal.hashing", "sldb.store.journal.layout", "sldb.store.journal.lock", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
