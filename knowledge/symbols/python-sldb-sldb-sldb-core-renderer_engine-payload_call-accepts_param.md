---
id: python-sldb-sldb-sldb-core-renderer_engine-payload_call-accepts_param
system: sldb
module: sldb.sldb.core.renderer_engine.payload_call
qualname: accepts_param
kind: FunctionDef
source_path: sldb/core/renderer_engine/payload_call.py
source_span: '34:48'
source_sha256: b80aaf3f6bb1c1f9db75c8dad70fe5a6404d1b08a456067451e8891613bcc2b9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer_engine.payload_call:accepts_param;
  contract-sha256:021f5b175ef8043e4d7070bebfe2391c6322807cc4c38976ec97118d902f2ab5
---

# accepts_param

## Signature

accepts_param(method: Any, name: str)

## Docstring

Whether a ``render_payload`` implementation takes the argument ``name``.

Args:
    method: The bound ``render_payload`` of a document instance.
    name: The keyword to look for.

Returns:
    True when the signature declares ``name`` or absorbs keywords.

## Imports

["__future__", "inspect", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
