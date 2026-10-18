---
id: python-sldb-sldb-core-segments-instrumented_render-render_with_spans
system: sldb
module: sldb.core.segments.instrumented_render
qualname: render_with_spans
kind: FunctionDef
source_path: sldb/core/segments/instrumented_render.py
source_span: '22:40'
source_sha256: f94161fc5f560cd0d37e3b1edefaf12ba66a3853687a28682c588de09bc4151f
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.segments.instrumented_render:render_with_spans;
  contract-sha256:78e06a0e05dce5ab4fcfba35246e739eb2e04c99f81be8fc99f8768e3f24c0bd
---

# render_with_spans

## Signature

render_with_spans(model_type: type, payload: dict[str, Any], ref_root: Path | None=None)

## Docstring

The canonical render of ``payload`` plus every value span in it.

Args:
    model_type: The ``StructuredNLDoc`` subclass to render through.
    payload: The payload to instantiate the model with.
    ref_root: Directory a composed field's refs resolve against — the project root.
        Without it they resolve against the working directory, so the same document
        segments differently depending on where the caller runs.

Returns:
    A tuple of the canonical text and a list of ``(meta, start, end)``, where
    ``meta`` carries the field ``path``, ``marker`` kind, ``traits`` and the
    wrap order under ``_order``.

## Imports

["__future__", "pathlib", "sldb.core.renderer", "sldb.core.renderer_engine.span_recorder", "typing"]

## Purpose

The canonical render of ``payload`` plus every value span in it.

## Architecture

Not documented.
