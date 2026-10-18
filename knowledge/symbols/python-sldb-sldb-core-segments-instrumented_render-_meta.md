---
id: python-sldb-sldb-core-segments-instrumented_render-_meta
system: sldb
module: sldb.core.segments.instrumented_render
qualname: _meta
kind: FunctionDef
source_path: sldb/core/segments/instrumented_render.py
source_span: '43:53'
source_sha256: f94161fc5f560cd0d37e3b1edefaf12ba66a3853687a28682c588de09bc4151f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.instrumented_render:_meta; contract-sha256:234dccf73dff32883de2dcefb4d6e9f3ba29bfeacc27547d65fb01a22c07b294
---

# _meta

## Signature

_meta(recorder: SpanRecorder, span_id: int)

## Docstring

The recorded metadata of one span, tagged with its wrap order.

Args:
    recorder: The recorder that collected the span.
    span_id: Index of the span in wrap order.

Returns:
    A copy of the metadata carrying ``_order``, the nesting tiebreak.

## Imports

["__future__", "pathlib", "sldb.core.renderer", "sldb.core.renderer_engine.span_recorder", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
