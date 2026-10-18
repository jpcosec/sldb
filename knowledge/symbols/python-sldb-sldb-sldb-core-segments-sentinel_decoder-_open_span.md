---
id: python-sldb-sldb-sldb-core-segments-sentinel_decoder-_open_span
system: sldb
module: sldb.sldb.core.segments.sentinel_decoder
qualname: _open_span
kind: FunctionDef
source_path: sldb/core/segments/sentinel_decoder.py
source_span: 60:74
source_sha256: 251c56399d88d64e3189be29334e03bd0b1777b3a4152101dbd676ede17a1ef9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.sentinel_decoder:_open_span;
  contract-sha256:4c31b8e619a284027dc95261a76e1a8619f20206afee3d1e838db421996dbc9b
---

# _open_span

## Signature

_open_span(raw: str, index: int, position: int, stack: list[tuple[int, int]])

## Docstring

Push the span opening at ``index`` and return the index after its header.

Args:
    raw: The full sentinel-marked text.
    index: Position of the ``OPEN`` sentinel.
    position: Offset in the decoded text where the span's value starts.
    stack: Open ``(span_id, start)`` pairs, mutated in place.

Returns:
    The index just past the ``SEP`` that closes the span header.

## Imports

["__future__", "sldb.core.renderer_engine.span_recorder"]

## Purpose

Not documented.

## Architecture

Not documented.
