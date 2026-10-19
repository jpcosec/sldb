---
id: python-sldb-sldb-store-journal-layout-journal_lock_path
system: sldb
module: sldb.store.journal.layout
qualname: journal_lock_path
kind: FunctionDef
source_path: sldb/store/journal/layout.py
source_span: '20:22'
source_sha256: e4e9c1f9c0cc91c0f79442c7e9c8eb6069d7b8189ab2704870230390c7d01d1b
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.journal.layout:journal_lock_path; contract-sha256:56cf174c0b9d300f2d8a3ca088b8f4ca0dfe3c6d8aa11d13f6fc5d2352668657
---

# journal_lock_path

## Signature

journal_lock_path(store_path: Path)

## Docstring

The advisory lock serializing journal appends, separate from the store index lock.

## Imports

["__future__", "pathlib", "sldb.store.layout"]

## Purpose

The advisory lock serializing journal appends, separate from the store index lock.

## Architecture

Not documented.
