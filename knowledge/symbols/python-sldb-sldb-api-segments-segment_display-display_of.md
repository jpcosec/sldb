---
id: python-sldb-sldb-api-segments-segment_display-display_of
system: sldb
module: sldb.api.segments.segment_display
qualname: display_of
kind: FunctionDef
source_path: sldb/api/segments/segment_display.py
source_span: '12:25'
source_sha256: c1f2f81cc30c07f7e7e0c6e152fca07acf151b5158c3809f703c0706539819da
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.segment_display:display_of; contract-sha256:34a1e4d6415afc8f91d73d1fc3d7ac9cfd03b14496a282906f50743317de226b
---

# display_of

## Signature

display_of(text: str, start: int, end: int)

## Docstring

Whether ``text[start:end]`` is a block of its own or sits inline.

Args:
    text: The canonical document text.
    start: Inclusive start offset of the field's surface.
    end: Exclusive end offset of the field's surface.

Returns:
    ``"block"`` when the field occupies its own block, else ``"inline"``.

## Imports

["__future__"]

## Purpose

Not documented.

## Architecture

Not documented.
