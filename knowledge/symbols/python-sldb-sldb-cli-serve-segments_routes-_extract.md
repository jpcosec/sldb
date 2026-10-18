---
id: python-sldb-sldb-cli-serve-segments_routes-_extract
system: sldb
module: sldb.cli.serve.segments_routes
qualname: _extract
kind: FunctionDef
source_path: sldb/cli/serve/segments_routes.py
source_span: 62:79
source_sha256: 0e885c9eff79cd20204b144ba8d39790f6b2fa50d2da4b9d870e156f9602ca62
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.segments_routes:_extract; contract-sha256:5ffb5e04fb207708d1335b9bcf93bfc1d541fcac5190738546b640ca9d26f201
---

# _extract

## Signature

_extract(store_path: Path, pythonpath: str, model: str, markdown: str)

## Docstring

Run the extraction, mapping each kind of failure to its own status.

Args:
    store_path: Path of the ``.sldb`` store being served.
    pythonpath: Import root for resolving the named model.
    model: Name of a model registered in the store.
    markdown: The raw markdown to read.

Returns:
    The serialized ``ExtractionSegments`` and 200, or a typed error body.

## Imports

["__future__", "pathlib", "sldb.api.segments", "sldb.core.exceptions", "typing"]

## Purpose

Run the extraction, mapping each kind of failure to its own status.

## Architecture

Not documented.
