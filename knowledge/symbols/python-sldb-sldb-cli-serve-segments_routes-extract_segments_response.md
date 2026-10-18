---
id: python-sldb-sldb-cli-serve-segments_routes-extract_segments_response
system: sldb
module: sldb.cli.serve.segments_routes
qualname: extract_segments_response
kind: FunctionDef
source_path: sldb/cli/serve/segments_routes.py
source_span: '43:59'
source_sha256: 0e885c9eff79cd20204b144ba8d39790f6b2fa50d2da4b9d870e156f9602ca62
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.segments_routes:extract_segments_response;
  contract-sha256:7e9b9f04b2c19286bf183139b4b216345a755f77adb9b503480fbf7283db9716
---

# extract_segments_response

## Signature

extract_segments_response(body: JsonDict, store_path: Path, pythonpath: str)

## Docstring

Answer ``POST /extract/segments`` with ``{model, markdown}``.

Args:
    body: The decoded JSON request body.
    store_path: Path of the ``.sldb`` store being served.
    pythonpath: Import root for resolving the named model.

Returns:
    The extraction and 200; 400 for a malformed body, 404 for a model that
    is not registered or cannot be imported, 422 for markdown that does not
    extract as that model.

## Imports

["__future__", "pathlib", "sldb.api.segments", "sldb.core.exceptions", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
