---
id: python-sldb-sldb-core-renderer_engine-payload_call-accepts_param
system: sldb
module: sldb.core.renderer_engine.payload_call
qualname: accepts_param
kind: FunctionDef
source_path: sldb/core/renderer_engine/payload_call.py
source_span: '34:48'
source_sha256: b80aaf3f6bb1c1f9db75c8dad70fe5a6404d1b08a456067451e8891613bcc2b9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.payload_call:accepts_param;
  contract-sha256:0b374812e8630cf11fd13ab13cbccbb77661e53830b29d47b3de6d3332850949
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

Whether a ``render_payload`` implementation takes the argument ``name``.

## Architecture

Not documented.
