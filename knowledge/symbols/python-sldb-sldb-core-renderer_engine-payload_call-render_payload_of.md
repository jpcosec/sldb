---
id: python-sldb-sldb-core-renderer_engine-payload_call-render_payload_of
system: sldb
module: sldb.core.renderer_engine.payload_call
qualname: render_payload_of
kind: FunctionDef
source_path: sldb/core/renderer_engine/payload_call.py
source_span: '18:31'
source_sha256: b80aaf3f6bb1c1f9db75c8dad70fe5a6404d1b08a456067451e8891613bcc2b9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.core.renderer_engine.payload_call:render_payload_of;
  contract-sha256:8fb0caff1cec145b51add302172880f1e75920e2c6c383f5d2807e9ede14f76b
---

# render_payload_of

## Signature

render_payload_of(model: Any, recorder: Any, ref_root: Path | None=None)

## Docstring

The model's render payload, passing only the arguments the model accepts.

Args:
    model: The document instance to take the payload from.
    recorder: The active ``SpanRecorder``, or None when not recording.
    ref_root: Directory composition refs resolve against, or None.

Returns:
    The payload mapping the renderer feeds to the template.

## Imports

["__future__", "inspect", "pathlib", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
