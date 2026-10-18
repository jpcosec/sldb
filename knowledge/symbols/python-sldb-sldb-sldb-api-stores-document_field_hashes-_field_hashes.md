---
id: python-sldb-sldb-sldb-api-stores-document_field_hashes-_field_hashes
system: sldb
module: sldb.sldb.api.stores.document_field_hashes
qualname: _field_hashes
kind: FunctionDef
source_path: sldb/api/stores/document_field_hashes.py
source_span: '26:38'
source_sha256: ead488d6aebfdbeb29692f6465bee59ec6145f1766a0b15b767f7841d27f6952
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.stores.document_field_hashes:_field_hashes;
  contract-sha256:3048d0111e8d88a6bf2577845d5c8bafec4a6fbc382faefe3428c34384dd3b2b
---

# _field_hashes

## Signature

_field_hashes(mtype: Any, m_name: str, doc: Any, text: str, force: bool=False)

## Docstring

The document's `content_hash` and its per-field map, from one extraction.

Both are empty when the Markdown no longer extracts (reported by `stores check`): an empty
map means "unknown", so a consumer comparing against it falls back to the whole document
rather than concluding no field moved.

## Imports

["__future__", "sldb.store.hashing", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
