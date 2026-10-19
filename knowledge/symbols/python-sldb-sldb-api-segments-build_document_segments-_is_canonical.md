---
id: python-sldb-sldb-api-segments-build_document_segments-_is_canonical
system: sldb
module: sldb.api.segments.build_document_segments
qualname: _is_canonical
kind: FunctionDef
source_path: sldb/api/segments/build_document_segments.py
source_span: 47:60
source_sha256: bda5832ce19e68ac1423df94831e354a74ed34a440de19840f14026df942d7a0
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.segments.build_document_segments:_is_canonical;
  contract-sha256:b228b16e1ac0da5eb9713b9a702ebc04dd860f148c50642aa0817066675b84b7
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

Whether the document file on disk already holds the canonical text.

## Architecture

Not documented.
