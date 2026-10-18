---
id: python-sldb-sldb-sldb-api-segments-segment_nodes-build_node
system: sldb
module: sldb.sldb.api.segments.segment_nodes
qualname: build_node
kind: FunctionDef
source_path: sldb/api/segments/segment_nodes.py
source_span: '21:40'
source_sha256: 395b7e3fa0ecb51cf1e811493c98e860fd4ae2cd9bf83bcccc2551d654056f1d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.segment_nodes:build_node; contract-sha256:cc32a923cffe9d93bc8f33e5817a6819b4c72cc52f85c2489b4832caf4e64048
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

Not documented.

## Architecture

Not documented.
