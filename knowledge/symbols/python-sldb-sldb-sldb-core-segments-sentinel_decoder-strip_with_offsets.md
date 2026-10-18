---
id: python-sldb-sldb-sldb-core-segments-sentinel_decoder-strip_with_offsets
system: sldb
module: sldb.sldb.core.segments.sentinel_decoder
qualname: strip_with_offsets
kind: FunctionDef
source_path: sldb/core/segments/sentinel_decoder.py
source_span: 77:89
source_sha256: 251c56399d88d64e3189be29334e03bd0b1777b3a4152101dbd676ede17a1ef9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.segments.sentinel_decoder:strip_with_offsets;
  contract-sha256:688b672b7a470f9514b1fd2695eb61096afc4691c112e0f18f3e64fd6d552c43
---

# strip_with_offsets

## Signature

strip_with_offsets(text: str, spans: list[Span])

## Docstring

Strip ``text`` the way the renderer does, clamping spans to the result.

Args:
    text: Decoded text, not yet stripped.
    spans: Spans addressed against ``text``.

Returns:
    The stripped text and the spans rebased on it.

## Imports

["__future__", "sldb.core.renderer_engine.span_recorder"]

## Purpose

Not documented.

## Architecture

Not documented.
