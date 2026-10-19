---
id: python-sldb-sldb-core-renderer_engine-jinja_trailing-unshield_trailing_newline
system: sldb
module: sldb.core.renderer_engine.jinja_trailing
qualname: unshield_trailing_newline
kind: FunctionDef
source_path: sldb/core/renderer_engine/jinja_trailing.py
source_span: '18:36'
source_sha256: 277c2fb390b8b776c11dedb31109164f8134712bf133c6e0f85750b136c27d4d
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.jinja_trailing:unshield_trailing_newline;
  contract-sha256:5f65ca525f2cfe98d550df02879f49f44ee13392b40875977c1433ac5f3cde68
---

# unshield_trailing_newline

## Signature

unshield_trailing_newline(text: str)

## Docstring

Move a sentinel-shielded trailing newline outside the sentinel group.

Exactly one newline is moved, which is exactly how many Jinja drops. Moving
the whole run would delete newlines the plain render keeps.

Args:
    text: A template line joined for rendering, sentinels included.

Returns:
    The text with one final shielded newline moved past the closing
    sentinels, letting Jinja drop it as it would without sentinels.

## Imports

["__future__", "sldb.core.renderer_engine.span_recorder"]

## Purpose

Move a sentinel-shielded trailing newline outside the sentinel group.

## Architecture

Not documented.
