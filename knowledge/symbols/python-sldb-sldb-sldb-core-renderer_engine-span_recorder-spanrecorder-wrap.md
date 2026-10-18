---
id: python-sldb-sldb-sldb-core-renderer_engine-span_recorder-spanrecorder-wrap
system: sldb
module: sldb.sldb.core.renderer_engine.span_recorder
qualname: SpanRecorder.wrap
kind: FunctionDef
source_path: sldb/core/renderer_engine/span_recorder.py
source_span: '27:38'
source_sha256: cdc8283006a58f8d13c955af17a5c823821a55c4439feb16859a25bc4fe06626
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer_engine.span_recorder:SpanRecorder.wrap;
  contract-sha256:edd5342f2dad0fc637e7f1cae81ccbf5ac5f77cdeeff15a2509ac7fb18247f1d
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

Not documented.

## Architecture

Not documented.
