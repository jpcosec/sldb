---
id: python-sldb-sldb-store-journal-append-append_entry
system: sldb
module: sldb.store.journal.append
qualname: append_entry
kind: FunctionDef
source_path: sldb/store/journal/append.py
source_span: '23:28'
source_sha256: 3bc2322e5dde4795c66c7339c0d7f2f9bf4bc49ba99fb54f7344ec742d3991a9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.journal.append:append_entry; contract-sha256:d65a31e782d61ab32476619561290709bcecf4584958774a7b55b4c45732f0aa
---

# append_entry

## Signature

append_entry(store_path: Path, data: dict[str, Any])

## Docstring

Record one write, chained to the journal's previous entry, under the journal lock.

## Imports

["__future__", "os", "pathlib", "sldb.store.io.utils", "sldb.store.journal.entry", "sldb.store.journal.hashing", "sldb.store.journal.layout", "sldb.store.journal.lock", "typing"]

## Purpose

Record one write, chained to the journal's previous entry, under the journal lock.

## Architecture

Not documented.
