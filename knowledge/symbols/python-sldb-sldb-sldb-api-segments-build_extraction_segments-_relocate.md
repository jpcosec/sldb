---
id: python-sldb-sldb-sldb-api-segments-build_extraction_segments-_relocate
system: sldb
module: sldb.sldb.api.segments.build_extraction_segments
qualname: _relocate
kind: FunctionDef
source_path: sldb/api/segments/build_extraction_segments.py
source_span: 68:86
source_sha256: 0ab9e4d6602c7ca475e0069d535cf6e1e4cb146d9b0c5aa325ce7915cd98eeed
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.build_extraction_segments:_relocate;
  contract-sha256:51410157442d452c20468996ecb3220adec0b6b9c78312e268f21811bc6fe935
---

# _relocate

## Signature

_relocate(node: dict[str, Any], markdown: str, opcodes: list[Any])

## Docstring

Re-address one canonical segment against the raw text.

Args:
    node: A segment dict built over the canonical text.
    markdown: The raw markdown to map onto.
    opcodes: The alignment between the two texts.

Returns:
    The field dict over raw offsets, or None for a composed piece, which
    has no address of its own in this payload.

## Imports

["__future__", "pathlib", "sldb.api.segments.extraction_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.canonical_alignment", "sldb.core.segments.instrumented_render", "sldb.core.segments.unmatched_runs", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
