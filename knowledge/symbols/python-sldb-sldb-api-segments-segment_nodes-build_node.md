---
id: python-sldb-sldb-api-segments-segment_nodes-build_node
system: sldb
module: sldb.api.segments.segment_nodes
qualname: build_node
kind: FunctionDef
source_path: sldb/api/segments/segment_nodes.py
source_span: '21:40'
source_sha256: 395b7e3fa0ecb51cf1e811493c98e860fd4ae2cd9bf83bcccc2551d654056f1d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.segment_nodes:build_node; contract-sha256:3de686f2f82a3a8130d6a447bfd4b04d89ff4b4e8d4976b84e184aefee42a521
---

# build_node

## Signature

build_node(meta: dict[str, Any], start: int, end: int, text: str, model_type: type, payload: dict[str, Any])

## Docstring

The segment dict for one recorded span.

Args:
    meta: Recorded span metadata, carrying ``path``, ``marker`` and ``_order``.
    start: Inclusive start offset of the span in ``text``.
    end: Exclusive end offset of the span in ``text``.
    text: The canonical document text.
    model_type: The model the document is rendered through.
    payload: The payload the text was rendered from.

Returns:
    A ``field`` or ``composition`` segment dict, ready for nesting.

## Imports

["__future__", "sldb.api.segments.payload_values", "sldb.api.segments.segment_display", "typing"]

## Purpose

The segment dict for one recorded span.

## Architecture

Not documented.
