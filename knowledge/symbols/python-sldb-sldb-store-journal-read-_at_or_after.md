---
id: python-sldb-sldb-store-journal-read-_at_or_after
system: sldb
module: sldb.store.journal.read
qualname: _at_or_after
kind: FunctionDef
source_path: sldb/store/journal/read.py
source_span: '30:34'
source_sha256: 29517a239f392ca54c98ccc92fc9b1994809a353a8b52b2812a4248fc7d75e6e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.journal.read:_at_or_after; contract-sha256:716ffb4b4fec212c0a2041022f535bfb50c73045b17a9465109c2abb5f746da2
---

# _at_or_after

## Signature

_at_or_after(timestamp: datetime, since: datetime)

## Docstring

Compare two timestamps, treating a naive one as UTC rather than raising.

## Imports

["__future__", "datetime", "pathlib", "sldb.store.io.utils", "sldb.store.journal.entry", "sldb.store.journal.layout"]

## Purpose

Compare two timestamps, treating a naive one as UTC rather than raising.

## Architecture

Not documented.
