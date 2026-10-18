---
id: python-sldb-sldb-api-segments-build_document_segments-build_document_segments
system: sldb
module: sldb.api.segments.build_document_segments
qualname: build_document_segments
kind: FunctionDef
source_path: sldb/api/segments/build_document_segments.py
source_span: '23:44'
source_sha256: bda5832ce19e68ac1423df94831e354a74ed34a440de19840f14026df942d7a0
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.build_document_segments:build_document_segments;
  contract-sha256:61000e0063e23ad9fe58af3854cd4dd145e7dae57fe45a7d8ea5b02957360579
---

# build_document_segments

## Signature

build_document_segments(store_path: Path, pythonpath: str | None, doc: str)

## Docstring

The segmented canonical render of a tracked document.

Args:
    store_path: Path of the ``.sldb`` store holding the document.
    pythonpath: Import root for resolving the document's model, or None.
    doc: Document reference: a name, a tracked path or ``Model/name``.

Returns:
    The document's literals and field spans over its canonical text.

Raises:
    ValueError: When the reference names no document or more than one.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_payload", "sldb.api.segments.document_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.instrumented_render", "sldb.core.segments.segment_tree", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
