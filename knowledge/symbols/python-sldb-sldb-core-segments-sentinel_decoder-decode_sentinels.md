---
id: python-sldb-sldb-core-segments-sentinel_decoder-decode_sentinels
system: sldb
module: sldb.core.segments.sentinel_decoder
qualname: decode_sentinels
kind: FunctionDef
source_path: sldb/core/segments/sentinel_decoder.py
source_span: '17:33'
source_sha256: 251c56399d88d64e3189be29334e03bd0b1777b3a4152101dbd676ede17a1ef9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.sentinel_decoder:decode_sentinels;
  contract-sha256:24686ff4ab1f62c26bacd3a48bedfbd92b102afb73a2b5be0fced3d471e9f9d2
---

# decode_sentinels

## Signature

decode_sentinels(raw: str)

## Docstring

Remove sentinels from ``raw`` and report where each span landed.

Args:
    raw: Rendered text containing ``U+E000 id U+E001 text U+E002`` groups.

Returns:
    The text without sentinels and a list of ``(span_id, start, end)``
    character offsets over that text.

## Imports

["__future__", "sldb.core.renderer_engine.span_recorder"]

## Purpose

Not documented.

## Architecture

Not documented.
