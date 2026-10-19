---
id: python-sldb-sldb-api-journal-journal
system: sldb
module: sldb.api.journal
qualname: journal
kind: FunctionDef
source_path: sldb/api/journal.py
source_span: '16:29'
source_sha256: ea653c7a1acc70c195d70f381b7cd582ac91ff1e266e4d25938445e20170ec2e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.journal:journal; contract-sha256:4b260712ef42110843ce31d231f5c299a500b34e4ecddf97aeb9dd4fbf5b403e
---

# journal

## Signature

journal(store: str | Path | None=None, limit: int | None=None, since: datetime | None=None, address: str | None=None)

## Docstring

Read a store's write journal, newest entry first.

Args:
    store: The store whose journal to read (path, alias, or None to discover it).
    limit: Return at most this many entries (the newest ones).
    since: Only entries at or after this UTC timestamp.
    address: Only entries for this `Model:doc` address (or model name).

Returns:
    The matching entries, newest first. An absent journal yields an empty list.

## Imports

["__future__", "datetime", "pathlib", "sldb.api.stores.open_store", "sldb.store.io", "sldb.store.io.shards", "sldb.store.journal", "sldb.store.layout", "typing"]

## Purpose

Read a store's write journal, newest entry first.

## Architecture

Not documented.
