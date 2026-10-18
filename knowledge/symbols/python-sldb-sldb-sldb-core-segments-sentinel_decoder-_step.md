---
id: python-sldb-sldb-sldb-core-segments-sentinel_decoder-_step
system: sldb
module: sldb.sldb.core.segments.sentinel_decoder
qualname: _step
kind: FunctionDef
source_path: sldb/core/segments/sentinel_decoder.py
source_span: '36:57'
source_sha256: 251c56399d88d64e3189be29334e03bd0b1777b3a4152101dbd676ede17a1ef9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.sentinel_decoder:_step; contract-sha256:338fd441758f7fc0041c70dc0703e8e807a74791f9fd6a33911b82d146615f78
---

# _step

## Signature

_step(raw: str, index: int, out: list[str], spans: list[Span], stack: list[tuple[int, int]])

## Docstring

Consume one character (or one opening sentinel) and return the next index.

Args:
    raw: The full sentinel-marked text.
    index: Position to read.
    out: Accumulator of decoded characters, mutated in place.
    spans: Accumulator of closed spans, mutated in place.
    stack: Open ``(span_id, start)`` pairs, mutated in place.

Returns:
    The index to read next.

## Imports

["__future__", "sldb.core.renderer_engine.span_recorder"]

## Purpose

Not documented.

## Architecture

Not documented.
