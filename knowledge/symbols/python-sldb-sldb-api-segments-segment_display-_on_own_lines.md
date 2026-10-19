---
id: python-sldb-sldb-api-segments-segment_display-_on_own_lines
system: sldb
module: sldb.api.segments.segment_display
qualname: _on_own_lines
kind: FunctionDef
source_path: sldb/api/segments/segment_display.py
source_span: '28:40'
source_sha256: c1f2f81cc30c07f7e7e0c6e152fca07acf151b5158c3809f703c0706539819da
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.segments.segment_display:_on_own_lines; contract-sha256:34abf4a57017d6e0801e9372e269f2468261b272537b886bb5f39bb161f33daf
---

# _on_own_lines

## Signature

_on_own_lines(text: str, start: int, end: int)

## Docstring

Whether the span starts at a line start and ends at a line end.

Args:
    text: The canonical document text.
    start: Inclusive start offset.
    end: Exclusive end offset.

Returns:
    True when no other text shares the span's first and last lines.

## Imports

["__future__"]

## Purpose

Whether the span starts at a line start and ends at a line end.

## Architecture

Not documented.
