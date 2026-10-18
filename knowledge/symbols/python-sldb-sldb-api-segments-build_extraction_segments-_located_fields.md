---
id: python-sldb-sldb-api-segments-build_extraction_segments-_located_fields
system: sldb
module: sldb.api.segments.build_extraction_segments
qualname: _located_fields
kind: FunctionDef
source_path: sldb/api/segments/build_extraction_segments.py
source_span: 50:65
source_sha256: 0ab9e4d6602c7ca475e0069d535cf6e1e4cb146d9b0c5aa325ce7915cd98eeed
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.build_extraction_segments:_located_fields;
  contract-sha256:5357f183d98b408d7e2810e4a5d07c204e7b62ab97e44bddba47215bb8d014ab
---

# _located_fields

## Signature

_located_fields(spans: list[Any], canonical: str, markdown: str, opcodes: list[Any], model_type: type, payload: dict[str, Any])

## Docstring

Every field span carried from the canonical text over to the raw text.

Args:
    spans: The ``(meta, start, end)`` spans of the instrumented render.
    canonical: The canonical text the spans address.
    markdown: The raw markdown to map onto.
    opcodes: The alignment between the two texts.
    model_type: The model being extracted with.
    payload: The extracted payload.

Returns:
    Field dicts addressed against the raw text, sorted by start offset.

## Imports

["__future__", "pathlib", "sldb.api.segments.extraction_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.canonical_alignment", "sldb.core.segments.instrumented_render", "sldb.core.segments.unmatched_runs", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
