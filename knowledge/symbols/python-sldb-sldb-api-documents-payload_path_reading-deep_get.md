---
id: python-sldb-sldb-api-documents-payload_path_reading-deep_get
system: sldb
module: sldb.api.documents.payload_path_reading
qualname: deep_get
kind: FunctionDef
source_path: sldb/api/documents/payload_path_reading.py
source_span: '32:49'
source_sha256: 790baf040577e9b1f216d1d8a8934dedd6b7e1a40033a4ac0a7d4149ad0b70f0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.payload_path_reading:deep_get; contract-sha256:4c787c2cdad0eb8626edeb14a788344fb9969dd35274a0b8aba62fa232387358
---

# deep_get

## Signature

deep_get(payload: Any, path: str)

## Docstring

The value at a dotted path; numeric segments index into lists.

Args:
    payload: A document payload (nested dicts and lists).
    path: Dotted path such as `address.city` or `items.0.name`.

Returns:
    The value found at the path.

Raises:
    SLDBFieldPathError: When a key is missing or a scalar is stepped into.
    IndexError: When a list index is out of range.

## Imports

["__future__", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
