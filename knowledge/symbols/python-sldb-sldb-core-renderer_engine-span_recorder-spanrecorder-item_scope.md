---
id: python-sldb-sldb-core-renderer_engine-span_recorder-spanrecorder-item_scope
system: sldb
module: sldb.core.renderer_engine.span_recorder
qualname: SpanRecorder.item_scope
kind: FunctionDef
source_path: sldb/core/renderer_engine/span_recorder.py
source_span: 67:82
source_sha256: cdc8283006a58f8d13c955af17a5c823821a55c4439feb16859a25bc4fe06626
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.span_recorder:SpanRecorder.item_scope;
  contract-sha256:1d36f870ca178e0e4dda17e9fe12c15ceadeda7794ac4fdb8c8dc194b1a7e16d
---

# SpanRecorder.item_scope

## Signature

item_scope(self, prefix: str, scalar_root: str | None)

## Docstring

Scope every path recorded inside to one list item.

Args:
    prefix: Path of the item, such as ``steps/2``.
    scalar_root: Root property name when the item is a scalar, else None.

Yields:
    None, with the prefix active for the duration of the block.

## Imports

["__future__", "contextlib", "typing"]

## Purpose

Scope every path recorded inside to one list item.

## Architecture

Not documented.
