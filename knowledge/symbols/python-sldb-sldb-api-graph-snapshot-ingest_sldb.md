---
id: python-sldb-sldb-api-graph-snapshot-ingest_sldb
system: sldb
module: sldb.api.graph.snapshot
qualname: ingest_sldb
kind: FunctionDef
source_path: sldb/api/graph/snapshot.py
source_span: '43:45'
source_sha256: f1ee6bb4d5245aab04d5624bc080beaa849e3eeb903896ca16e9278dd0ec747e
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.api.graph.snapshot:ingest_sldb; contract-sha256:cf75db3d5ab19e424aa86e8a8b962d83b1a2914cc4f3801e96f00116c33184eb
---

# ingest_sldb

## Signature

ingest_sldb(payload: dict[str, Any])

## Docstring

Convert an `sldb_kgdb_semantic_export` v1 payload (or one written under its old name) into a GraphSnapshot.

## Imports

["__future__", "sldb.api.edges.edge_reading", "sldb.api.stores.open_store", "sldb.store.edge_index.federation", "sldb.store.export", "sldb.store.graph.convert", "sldb.store.graph.graph_io", "sldb.store.graph.ingest_sldb", "sldb.store.graph.snapshot", "typing"]

## Purpose

Convert an `sldb_kgdb_semantic_export` v1 payload (or one written under its old name) into a GraphSnapshot.

## Architecture

Not documented.
