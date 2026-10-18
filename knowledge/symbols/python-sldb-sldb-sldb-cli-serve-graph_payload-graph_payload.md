---
id: python-sldb-sldb-sldb-cli-serve-graph_payload-graph_payload
system: sldb
module: sldb.sldb.cli.serve.graph_payload
qualname: graph_payload
kind: FunctionDef
source_path: sldb/cli/serve/graph_payload.py
source_span: '34:48'
source_sha256: 5b6ff19cdd49719215b9d0f0fe7a03a57c91680f246042ba74ad005a4c0f3cd7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.cli.serve.graph_payload:graph_payload; contract-sha256:b1b5026c604c9e7e2688eeafebcf443b340ff4f1424717d37263f601c49cb48e
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

Not documented.

## Architecture

Not documented.
