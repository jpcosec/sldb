---
id: python-sldb-sldb-sldb-core-renderer-sldbrenderer-render_raw
system: sldb
module: sldb.sldb.core.renderer
qualname: SLDBRenderer.render_raw
kind: FunctionDef
source_path: sldb/core/renderer.py
source_span: '37:50'
source_sha256: ca9068edcc01fd6be31a3a6b103846c31ac742cca66e4df3bc71aaf3aa6fb2a5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.core.renderer:SLDBRenderer.render_raw; contract-sha256:a9b311b49a2ab01bdfa0776285378a32ce88ac5f3d3830bbb14b2727fd9ae134
---

# SLDBRenderer.render_raw

## Signature

render_raw(self, model: StructuredNLDoc, ref_root: Path | None=None)

## Docstring

The joined blocks before stripping, sentinels included when recording.

Args:
    model: The document instance to render.
    ref_root: Directory composition refs resolve against, or None for the CWD.

Returns:
    The rendered blocks joined by blank lines, not yet stripped.

## Imports

["__future__", "jinja2", "pathlib", "sldb.core.ast", "sldb.core.handlers.router", "sldb.core.node", "sldb.core.renderer_engine.list", "sldb.core.renderer_engine.payload_call", "sldb.core.renderer_engine.table", "sldb.core.renderer_engine.yaml", "sldb.core.segments.sentinel_decoder", "sldb.models.structured_doc", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
