---
id: python-sldb-sldb-api-segments-build_document_segments-_read_stripped
system: sldb
module: sldb.api.segments.build_document_segments
qualname: _read_stripped
kind: FunctionDef
source_path: sldb/api/segments/build_document_segments.py
source_span: 63:76
source_sha256: bda5832ce19e68ac1423df94831e354a74ed34a440de19840f14026df942d7a0
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.segments.build_document_segments:_read_stripped;
  contract-sha256:3a23a38d71819a47cc03c282b489b5c5fdbb8113318ecce3fe59a8df2def99fc
---

# _read_stripped

## Signature

_read_stripped(file_path: Path, text: str)

## Docstring

Compare a file's stripped contents with ``text``.

Args:
    file_path: Absolute path of the document file.
    text: The canonical render to compare against.

Returns:
    The comparison result, or None when the file cannot be read.

## Imports

["__future__", "pathlib", "sldb.api.documents.document_payload", "sldb.api.segments.document_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.instrumented_render", "sldb.core.segments.segment_tree", "typing"]

## Purpose

Compare a file's stripped contents with ``text``.

## Architecture

Not documented.
