---
id: python-sldb-sldb-api-edges-edge_reading-edges_from
system: sldb
module: sldb.api.edges.edge_reading
qualname: edges_from
kind: FunctionDef
source_path: sldb/api/edges/edge_reading.py
source_span: '31:44'
source_sha256: 843bafb03f66570ae4a91c980e7c72edc694998e17af5edc4882a34b62ba45b5
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.api.edges.edge_reading:edges_from; contract-sha256:7bef0d4a088f6d7e66f94117d06aae79a06037348577c62c3c3ba0e0d29a9e55
---

# edges_from

## Signature

edges_from(store: str | Path | None, export_id: str, relation: str | None=None, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

Edges leaving a document (`Model:name`) or any node (`sldb://<kind>/...`).

Args:
    store: The store (path, alias, or None to discover it).
    export_id: A document's export id, or a full node id.
    relation: Only edges of this relation type; None for all.
    include_linked: As in `load_edge_index`.
    exclude_tags: As in `load_edge_index`.

Returns:
    `{source, target, relation, metadata}` records, in a stable order.

## Imports

["__future__", "pathlib", "sldb.api.stores.open_store", "sldb.store.edge_index.compose", "sldb.store.edge_index.edge_index", "sldb.store.models", "typing"]

## Purpose

Edges leaving a document (`Model:name`) or any node (`sldb://<kind>/...`).

## Architecture

Not documented.
