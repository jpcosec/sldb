---
id: python-sldb-sldb-core-segments-sentinel_decoder-_clamp
system: sldb
module: sldb.core.segments.sentinel_decoder
qualname: _clamp
kind: FunctionDef
source_path: sldb/core/segments/sentinel_decoder.py
source_span: 92:102
source_sha256: 251c56399d88d64e3189be29334e03bd0b1777b3a4152101dbd676ede17a1ef9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.sentinel_decoder:_clamp; contract-sha256:5518767b3a28a6fd4f4e6076db82398482abaad7a41c3350168d872a71481a2b
---

# _clamp

## Signature

_clamp(position: int, stripped: str)

## Docstring

Keep an offset inside the stripped text.

Args:
    position: Candidate offset, already rebased by the leading whitespace.
    stripped: The stripped text the offset addresses.

Returns:
    ``position`` bounded to ``[0, len(stripped)]``.

## Imports

["__future__", "sldb.core.renderer_engine.span_recorder"]

## Purpose

Keep an offset inside the stripped text.

## Architecture

Not documented.
