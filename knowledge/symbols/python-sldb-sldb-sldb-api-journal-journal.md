---
id: python-sldb-sldb-sldb-api-journal-journal
system: sldb
module: sldb.sldb.api.journal
qualname: journal
kind: FunctionDef
source_path: sldb/api/journal.py
source_span: '16:29'
source_sha256: ea653c7a1acc70c195d70f381b7cd582ac91ff1e266e4d25938445e20170ec2e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.journal:journal; contract-sha256:d4e238a280cc891fdef97e44faeb0a257c057c28c60bd4d68cff97b2340af6d1
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

Not documented.

## Architecture

Not documented.
