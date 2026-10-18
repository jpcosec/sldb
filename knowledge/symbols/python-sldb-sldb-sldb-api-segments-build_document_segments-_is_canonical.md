---
id: python-sldb-sldb-sldb-api-segments-build_document_segments-_is_canonical
system: sldb
module: sldb.sldb.api.segments.build_document_segments
qualname: _is_canonical
kind: FunctionDef
source_path: sldb/api/segments/build_document_segments.py
source_span: 47:60
source_sha256: bda5832ce19e68ac1423df94831e354a74ed34a440de19840f14026df942d7a0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.build_document_segments:_is_canonical;
  contract-sha256:70f1c3e44fd89f956d44c50ea1b6d9d74adea7cea6c1774dcfe7150be728c115
---

# _is_canonical

## Signature

_is_canonical(store_path: Path, path: str | None, text: str)

## Docstring

Whether the document file on disk already holds the canonical text.

Args:
    store_path: Path of the store, whose parent is the project root.
    path: The document's path relative to that root, or None.
    text: The canonical render to compare against.

Returns:
    True or False after a successful read, None when the file is unreadable.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_payload", "sldb.api.segments.document_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.instrumented_render", "sldb.core.segments.segment_tree", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
