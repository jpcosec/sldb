---
id: python-sldb-sldb-api-records-record_serialization-select_keys
system: sldb
module: sldb.api.records.record_serialization
qualname: select_keys
kind: FunctionDef
source_path: sldb/api/records/record_serialization.py
source_span: '27:30'
source_sha256: 1b1a6e53bc3987063522a41fa6abce066033f581906883d84eea29023b91a6a8
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.records.record_serialization:select_keys; contract-sha256:6eebed3ff8edcd7dbfbe97419195fb33623df5f0c2467f95f5fd836a4d892c7f
---

# select_keys

## Signature

select_keys(payload: list[dict[str, Any]], select: str)

## Docstring

Narrow each mapping to the comma-separated keys in `select`, missing keys as None.

## Imports

["__future__", "sldb.api.records.search_record", "typing"]

## Purpose

Narrow each mapping to the comma-separated keys in `select`, missing keys as None.

## Architecture

Not documented.
