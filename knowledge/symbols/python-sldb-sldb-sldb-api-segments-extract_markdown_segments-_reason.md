---
id: python-sldb-sldb-sldb-api-segments-extract_markdown_segments-_reason
system: sldb
module: sldb.sldb.api.segments.extract_markdown_segments
qualname: _reason
kind: FunctionDef
source_path: sldb/api/segments/extract_markdown_segments.py
source_span: '45:56'
source_sha256: e22d23b5bf5399393f23878e71b52f36ff4a90ef85b59c19b1fe536f9ce8be5d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.segments.extract_markdown_segments:_reason;
  contract-sha256:1dc3cb391b2eddaa3207aa5fa4e5ae1ec697b26296cbe896bf2333791409a735
---

# _reason

## Signature

_reason(model: str, exc: Exception)

## Docstring

A message saying the markdown, not the model, is what failed.

Args:
    model: Name of the model the markdown was read with.
    exc: The error extraction raised.

Returns:
    A single-line, human-readable explanation.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.load_registered_model", "sldb.api.segments.build_extraction_segments", "sldb.api.segments.extraction_segments", "sldb.core.exceptions"]

## Purpose

Not documented.

## Architecture

Not documented.
