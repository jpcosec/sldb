---
id: python-sldb-sldb-core-renderer-sldbrenderer-render
system: sldb
module: sldb.core.renderer
qualname: SLDBRenderer.render
kind: FunctionDef
source_path: sldb/core/renderer.py
source_span: '28:35'
source_sha256: ca9068edcc01fd6be31a3a6b103846c31ac742cca66e4df3bc71aaf3aa6fb2a5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.renderer:SLDBRenderer.render; contract-sha256:6d09a64e9a483e5f7786c418793c0eee69aebd6c2255d48dde8dbabbdca9390d
---

# SLDBRenderer.render

## Signature

render(self, model: StructuredNLDoc, ref_root: Path | None=None)

## Docstring

Renders the model to a Markdown string. `ref_root` resolves composition refs.

## Imports

["__future__", "jinja2", "pathlib", "sldb.core.ast", "sldb.core.handlers.router", "sldb.core.node", "sldb.core.renderer_engine.list", "sldb.core.renderer_engine.payload_call", "sldb.core.renderer_engine.table", "sldb.core.renderer_engine.yaml", "sldb.core.segments.sentinel_decoder", "sldb.models.structured_doc", "typing"]

## Purpose

Renders the model to a Markdown string. `ref_root` resolves composition refs.

## Architecture

Not documented.
