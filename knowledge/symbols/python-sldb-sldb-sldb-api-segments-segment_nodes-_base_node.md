---
id: python-sldb-sldb-sldb-api-segments-segment_nodes-_base_node
system: sldb
module: sldb.sldb.api.segments.segment_nodes
qualname: _base_node
kind: FunctionDef
source_path: sldb/api/segments/segment_nodes.py
source_span: 43:62
source_sha256: 395b7e3fa0ecb51cf1e811493c98e860fd4ae2cd9bf83bcccc2551d654056f1d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.segment_nodes:_base_node; contract-sha256:b7546bce9f9601fe571fdb3ff93761fc6eeb7235c1d97561c584a3598d105157
---

# _base_node

## Signature

_base_node(meta: dict[str, Any], start: int, end: int, text: str)

## Docstring

The keys every recorded segment carries, whatever its type.

Args:
    meta: Recorded span metadata.
    start: Inclusive start offset of the span in ``text``.
    end: Exclusive end offset of the span in ``text``.
    text: The canonical document text.

Returns:
    A segment dict without value, kind or composition details.

## Imports

["__future__", "sldb.api.segments.payload_values", "sldb.api.segments.segment_display", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
