---
id: python-sldb-sldb-store-journal-read-read_entries
system: sldb
module: sldb.store.journal.read
qualname: read_entries
kind: FunctionDef
source_path: sldb/store/journal/read.py
source_span: '13:20'
source_sha256: 29517a239f392ca54c98ccc92fc9b1994809a353a8b52b2812a4248fc7d75e6e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.journal.read:read_entries; contract-sha256:fb6660bfcd0e2cdbce97c76a96cc7382b0681e52b8f7d9f120939b2f9c22d998
---

# read_entries

## Signature

read_entries(store_path: Path, limit: int | None=None, since: datetime | None=None, address: str | None=None)

## Docstring

Newest-first entries; `since` and `address` narrow the result before `limit` cuts it.

## Imports

["__future__", "datetime", "pathlib", "sldb.store.io.utils", "sldb.store.journal.entry", "sldb.store.journal.layout"]

## Purpose

Newest-first entries; `since` and `address` narrow the result before `limit` cuts it.

## Architecture

Not documented.
