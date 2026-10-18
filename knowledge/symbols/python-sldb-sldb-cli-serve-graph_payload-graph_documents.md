---
id: python-sldb-sldb-cli-serve-graph_payload-graph_documents
system: sldb
module: sldb.cli.serve.graph_payload
qualname: graph_documents
kind: FunctionDef
source_path: sldb/cli/serve/graph_payload.py
source_span: '20:31'
source_sha256: 5b6ff19cdd49719215b9d0f0fe7a03a57c91680f246042ba74ad005a4c0f3cd7
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.cli.serve.graph_payload:graph_documents; contract-sha256:46872e78b4fd7c2b56c76d624de2753607469682eb2dbefbe47a565a81a32dbf
---

# graph_documents

## Signature

graph_documents(store_path: Path, pythonpath: str)

## Docstring

Every tracked document of the store, serialized for the graph surface.

Args:
    store_path: Path of the ``.sldb`` store being served.
    pythonpath: Import root for resolving the document models.

Returns:
    One serialized record per document that could be loaded.

## Imports

["__future__", "pathlib", "sldb.api", "sldb.cli.model_utils", "sldb.cli.serve.unavailable_models", "sldb.store.query", "typing"]

## Purpose

Not documented.

## Architecture

Not documented.
