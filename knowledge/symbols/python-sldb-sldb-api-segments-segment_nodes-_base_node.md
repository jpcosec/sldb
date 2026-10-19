---
id: python-sldb-sldb-api-segments-segment_nodes-_base_node
system: sldb
module: sldb.api.segments.segment_nodes
qualname: _base_node
kind: FunctionDef
source_path: sldb/api/segments/segment_nodes.py
source_span: 43:62
source_sha256: 395b7e3fa0ecb51cf1e811493c98e860fd4ae2cd9bf83bcccc2551d654056f1d
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.segments.segment_nodes:_base_node; contract-sha256:9a33b39b165d03767adbcf9f2765bdb40875685e289ff77b5a22bdaa6eed6782
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

The keys every recorded segment carries, whatever its type.

## Architecture

Not documented.
