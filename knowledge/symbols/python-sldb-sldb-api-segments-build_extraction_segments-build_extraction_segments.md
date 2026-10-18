---
id: python-sldb-sldb-api-segments-build_extraction_segments-build_extraction_segments
system: sldb
module: sldb.api.segments.build_extraction_segments
qualname: build_extraction_segments
kind: FunctionDef
source_path: sldb/api/segments/build_extraction_segments.py
source_span: '22:47'
source_sha256: 0ab9e4d6602c7ca475e0069d535cf6e1e4cb146d9b0c5aa325ce7915cd98eeed
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.build_extraction_segments:build_extraction_segments;
  contract-sha256:3e65676fda5871127af52c13818a43d6b5189377ec7ecea5251c7c8e43e4e718
---

# build_extraction_segments

## Signature

build_extraction_segments(model_type: type, markdown: str, ref_root: Path | None=None)

## Docstring

The fields of ``model_type`` located in ``markdown``.

Args:
    model_type: The ``StructuredNLDoc`` subclass to extract with.
    markdown: The raw markdown to read.
    ref_root: Directory a composed field's refs resolve against, or None.

Returns:
    The extracted payload, the canonical render, and every field's span over
    the raw text with its alignment quality and the overall coverage.

Raises:
    Exception: Whatever extraction raises when the markdown does not satisfy
        the model; callers at a boundary are expected to classify it.

## Imports

["__future__", "pathlib", "sldb.api.segments.extraction_segments", "sldb.api.segments.segment_nodes", "sldb.core.segments.canonical_alignment", "sldb.core.segments.instrumented_render", "sldb.core.segments.unmatched_runs", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
