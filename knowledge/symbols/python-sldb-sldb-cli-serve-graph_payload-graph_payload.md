---
id: python-sldb-sldb-cli-serve-graph_payload-graph_payload
system: sldb
module: sldb.cli.serve.graph_payload
qualname: graph_payload
kind: FunctionDef
source_path: sldb/cli/serve/graph_payload.py
source_span: '34:48'
source_sha256: 5b6ff19cdd49719215b9d0f0fe7a03a57c91680f246042ba74ad005a4c0f3cd7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.graph_payload:graph_payload; contract-sha256:43e7778a82b8d10f78b55c5aa185d0e72414898a80081c25b9a94bf4cad60817
---

# graph_payload

## Signature

graph_payload(store_path: Path, pythonpath: str)

## Docstring

The documents of the store together with any unavailable models.

Args:
    store_path: Path of the ``.sldb`` store being served.
    pythonpath: Import root for resolving the document models.

Returns:
    ``{documents, unavailable}``; ``unavailable`` is empty for a healthy store.

## Imports

["__future__", "pathlib", "sldb.api", "sldb.cli.model_utils", "sldb.cli.serve.unavailable_models", "sldb.store.query", "typing"]

## Purpose

The documents of the store together with any unavailable models.

## Architecture

Not documented.
