---
id: python-sldb-sldb-api-segments-extract_markdown_segments-extract_markdown_segments
system: sldb
module: sldb.api.segments.extract_markdown_segments
qualname: extract_markdown_segments
kind: FunctionDef
source_path: sldb/api/segments/extract_markdown_segments.py
source_span: '20:42'
source_sha256: e22d23b5bf5399393f23878e71b52f36ff4a90ef85b59c19b1fe536f9ce8be5d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.segments.extract_markdown_segments:extract_markdown_segments;
  contract-sha256:65431fe53aed0e53bd227a1597c32e65177f2cab24ee6d33f9c3314358818550
---

# extract_markdown_segments

## Signature

extract_markdown_segments(store_path: Path, pythonpath: str | None, model: str, markdown: str)

## Docstring

Locate the fields of a registered model inside raw markdown.

Args:
    store_path: Path of the ``.sldb`` store the model is registered in.
    pythonpath: Import root for resolving the model class, or None.
    model: Name of a model registered in the store.
    markdown: The raw markdown to read.

Returns:
    The extraction with every field's span over the raw text.

Raises:
    SLDBStoreError: When no such model is registered in the store.
    SLDBModelError: When the registered model class cannot be imported.
    SLDBValidationError: When the markdown does not satisfy the model; the
        underlying reason is kept in ``details``.

## Imports

["__future__", "pathlib", "sldb.api.model_registry.load_registered_model", "sldb.api.segments.build_extraction_segments", "sldb.api.segments.extraction_segments", "sldb.core.exceptions"]

## Purpose

Locate the fields of a registered model inside raw markdown.

## Architecture

Not documented.
