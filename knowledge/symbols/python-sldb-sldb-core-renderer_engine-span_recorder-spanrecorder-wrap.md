---
id: python-sldb-sldb-core-renderer_engine-span_recorder-spanrecorder-wrap
system: sldb
module: sldb.core.renderer_engine.span_recorder
qualname: SpanRecorder.wrap
kind: FunctionDef
source_path: sldb/core/renderer_engine/span_recorder.py
source_span: '27:38'
source_sha256: cdc8283006a58f8d13c955af17a5c823821a55c4439feb16859a25bc4fe06626
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.span_recorder:SpanRecorder.wrap;
  contract-sha256:cc4cbf2d4794c754baddea99cd01bfa46a77261b14584f64f435d0f96811b863
---

# SpanRecorder.wrap

## Signature

wrap(self, text: str, meta: dict[str, Any])

## Docstring

Register ``meta`` and return ``text`` wrapped in sentinels.

Args:
    text: The rendered surface of a value; may be empty.
    meta: Metadata for the span (path, marker kind, traits...).

Returns:
    The sentinel-wrapped text carrying the new span id.

## Imports

["__future__", "contextlib", "typing"]

## Purpose

Register ``meta`` and return ``text`` wrapped in sentinels.

## Architecture

Not documented.
