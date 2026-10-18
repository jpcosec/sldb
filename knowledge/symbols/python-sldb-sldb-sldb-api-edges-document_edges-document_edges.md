---
id: python-sldb-sldb-sldb-api-edges-document_edges-document_edges
system: sldb
module: sldb.sldb.api.edges.document_edges
qualname: document_edges
kind: FunctionDef
source_path: sldb/api/edges/document_edges.py
source_span: '15:33'
source_sha256: 9b931be59a24ab5c1bcdf66fb84a838a91f4178c8d9799b8f23d390e319aa09e
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.api.edges.document_edges:document_edges; contract-sha256:a38c5e960c324d2fcfa6ffb909dc649a3452be1fd5e1631f40155931c0424b3b
---

# document_edges

## Signature

document_edges(store: str | Path | None, pythonpath: str | None=None, doc_id: str | None=None)

## Docstring

Rebuild the edge index, then list the edges that join two documents.

Edges with a non-document end (tags, models, fields, the store) are left out.
Authored edges the index rejected stay out too: they are `EdgeIndex.problems`,
reported by `check_edges`, and never break this read.

Args:
    store: The store (path, alias, or None to discover it).
    pythonpath: Directory to import the store's model modules from.
    doc_id: Only edges where this document (`Model:name`) is source or target.

Returns:
    The edges in the index's stable order.

## Imports

["__future__", "pathlib", "sldb.api.edges.document_edge", "sldb.api.edges.edge_reading", "sldb.api.edges.rebuild_edges", "sldb.store.models.edge_record"]

## Purpose

Not documented.

## Architecture

Not documented.
