---
id: python-sldb-sldb-core-renderer_engine-span_recorder-spanrecorder-meta_for
system: sldb
module: sldb.core.renderer_engine.span_recorder
qualname: SpanRecorder.meta_for
kind: FunctionDef
source_path: sldb/core/renderer_engine/span_recorder.py
source_span: 55:64
source_sha256: cdc8283006a58f8d13c955af17a5c823821a55c4439feb16859a25bc4fe06626
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.span_recorder:SpanRecorder.meta_for;
  contract-sha256:a4e37cac8dcf20cbf8e59fae1c142951846a79e239fa8199c6ae8563c7cb499e
---

# SpanRecorder.meta_for

## Signature

meta_for(self, marker: Any)

## Docstring

Span metadata for a parsed marker at the current prefix.

Args:
    marker: A parsed ``Marker`` from ``sldb.core.handlers.utils``.

Returns:
    A mapping with the field ``path``, the ``marker`` kind and its ``traits``.

## Imports

["__future__", "contextlib", "typing"]

## Purpose

Span metadata for a parsed marker at the current prefix.

## Architecture

Not documented.
