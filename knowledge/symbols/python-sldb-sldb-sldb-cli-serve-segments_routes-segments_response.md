---
id: python-sldb-sldb-sldb-cli-serve-segments_routes-segments_response
system: sldb
module: sldb.sldb.cli.serve.segments_routes
qualname: segments_response
kind: FunctionDef
source_path: sldb/cli/serve/segments_routes.py
source_span: '26:40'
source_sha256: 0e885c9eff79cd20204b144ba8d39790f6b2fa50d2da4b9d870e156f9602ca62
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.segments_routes:segments_response;
  contract-sha256:ccf7888494b1ddf03a10f045dffa8e1db4a9dd2e6070eb32f947f47e14bd78f7
---

# segments_response

## Signature

segments_response(store_path: Path, pythonpath: str, name: str)

## Docstring

The segments of a tracked document, or a 422 when it does not render.

Args:
    store_path: Path of the ``.sldb`` store being served.
    pythonpath: Import root for resolving the document's model.
    name: The tracked document's name.

Returns:
    The serialized ``DocumentSegments`` and 200, or an error body and 422.

## Imports

["__future__", "pathlib", "sldb.api.segments", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
