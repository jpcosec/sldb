---
id: python-sldb-sldb-sldb-api-segments-build_extraction_segments-_coverage
system: sldb
module: sldb.sldb.api.segments.build_extraction_segments
qualname: _coverage
kind: FunctionDef
source_path: sldb/api/segments/build_extraction_segments.py
source_span: 89:100
source_sha256: 0ab9e4d6602c7ca475e0069d535cf6e1e4cb146d9b0c5aa325ce7915cd98eeed
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.build_extraction_segments:_coverage;
  contract-sha256:642c7d02e23eab7ec1f8ffb35531cf7e53ef8c9ff3a7b39841e0499794f6d7b6
---

# _coverage

## Signature

_coverage(fields: list[dict[str, Any]], markdown: str)

## Docstring

Fraction of the raw text's meaningful length that fields cover.

Args:
    fields: The located field dicts.
    markdown: The raw markdown they address.

Returns:
    A value in ``[0, 1]``; the denominator ignores border whitespace.

## Imports

["__future__", "pathlib", "sldb.api.segments.extraction_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.canonical_alignment", "sldb.core.segments.instrumented_render", "sldb.core.segments.unmatched_runs", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
