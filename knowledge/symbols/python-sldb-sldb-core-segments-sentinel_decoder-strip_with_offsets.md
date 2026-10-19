---
id: python-sldb-sldb-core-segments-sentinel_decoder-strip_with_offsets
system: sldb
module: sldb.core.segments.sentinel_decoder
qualname: strip_with_offsets
kind: FunctionDef
source_path: sldb/core/segments/sentinel_decoder.py
source_span: 77:89
source_sha256: 251c56399d88d64e3189be29334e03bd0b1777b3a4152101dbd676ede17a1ef9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.segments.sentinel_decoder:strip_with_offsets;
  contract-sha256:36958d8e25b95dc6ca6dbcc577c1aa82174f8f74a81e4b026a8f7d27d4810c33
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

Strip ``text`` the way the renderer does, clamping spans to the result.

## Architecture

Not documented.
