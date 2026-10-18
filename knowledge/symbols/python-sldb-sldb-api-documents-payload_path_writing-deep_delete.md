---
id: python-sldb-sldb-api-documents-payload_path_writing-deep_delete
system: sldb
module: sldb.api.documents.payload_path_writing
qualname: deep_delete
kind: FunctionDef
source_path: sldb/api/documents/payload_path_writing.py
source_span: 80:99
source_sha256: 92d8f3002e9c87f191ccba68ee806f67d467f0756249b11b1d4b44a08944382e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.payload_path_writing:deep_delete;
  contract-sha256:1db2306020b5af999b8bfb40449e87e6869968c79068049466cc7b5076bcf93b
---

# deep_delete

## Signature

deep_delete(payload: Any, path: str)

## Docstring

Remove the value at a dotted path, in place.

Args:
    payload: A document payload (nested dicts and lists).
    path: Dotted path; numeric segments index into lists.

Returns:
    The same payload, mutated.

Raises:
    SLDBFieldPathError: When an intermediate key is missing.
    IndexError: When a list index is out of range.

## Imports

["__future__", "sldb.api.documents.payload_path_reading", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
