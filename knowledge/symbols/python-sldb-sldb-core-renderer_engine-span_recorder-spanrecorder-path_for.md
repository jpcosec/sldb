---
id: python-sldb-sldb-core-renderer_engine-span_recorder-spanrecorder-path_for
system: sldb
module: sldb.core.renderer_engine.span_recorder
qualname: SpanRecorder.path_for
kind: FunctionDef
source_path: sldb/core/renderer_engine/span_recorder.py
source_span: '40:53'
source_sha256: cdc8283006a58f8d13c955af17a5c823821a55c4439feb16859a25bc4fe06626
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.span_recorder:SpanRecorder.path_for;
  contract-sha256:607eed6654ac0ef7831ddff41a898aef7b63dba68a0a1087ceaba19238081880
---

# SpanRecorder.path_for

## Signature

path_for(self, name: str)

## Docstring

Field path of ``name`` under the active list-item prefix.

Args:
    name: The marker's property name.

Returns:
    ``name`` at the root, ``root/i`` for a scalar item, else ``root/i/name``.

## Imports

["__future__", "contextlib", "typing"]

## Purpose

Field path of ``name`` under the active list-item prefix.

## Architecture

Not documented.
