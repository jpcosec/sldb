---
id: python-sldb-sldb-api-documents-payload_path_writing-deep_set
system: sldb
module: sldb.api.documents.payload_path_writing
qualname: deep_set
kind: FunctionDef
source_path: sldb/api/documents/payload_path_writing.py
source_span: 48:67
source_sha256: 92d8f3002e9c87f191ccba68ee806f67d467f0756249b11b1d4b44a08944382e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.documents.payload_path_writing:deep_set; contract-sha256:294834d24e411000711c99292da3ce60595f2bbeb9cee49f2a1e006250b13c7b
---

# deep_set

## Signature

deep_set(payload: Any, path: str, new_value: Any, create: bool=False)

## Docstring

Assign the value at a dotted path, in place.

Args:
    payload: A document payload (nested dicts and lists).
    path: Dotted path; numeric segments index into lists.
    new_value: The value to assign.
    create: Create missing dict keys (intermediate ones as empty dicts).

Returns:
    The same payload, mutated.

Raises:
    SLDBFieldPathError: When a key is missing and `create` is False.
    IndexError: When a list index is out of range.

## Imports

["__future__", "sldb.api.documents.payload_path_reading", "sldb.core.exceptions", "typing"]

## Purpose

Assign the value at a dotted path, in place.

## Architecture

Not documented.
