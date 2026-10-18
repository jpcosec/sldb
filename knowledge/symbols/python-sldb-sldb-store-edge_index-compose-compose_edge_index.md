---
id: python-sldb-sldb-store-edge_index-compose-compose_edge_index
system: sldb
module: sldb.store.edge_index.compose
qualname: compose_edge_index
kind: FunctionDef
source_path: sldb/store/edge_index/compose.py
source_span: '22:40'
source_sha256: 6559b58c4c44b90f19dc0c8ca82dceb7eb91725eb62eb34819dd9a2a62b03661
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.compose:compose_edge_index; contract-sha256:ec8b4ff2bb615cc1a8945ea93aed66371a5ef16414c788a7bff9c5d4aee026a3
---

# compose_edge_index

## Signature

compose_edge_index(store_path: Path, include_linked: bool=True, exclude_tags: Iterable[str]=())

## Docstring

The store's edge index, read from its shards (never rebuilt here).

Args:
    store_path: The store's `.sldb` directory.
    include_linked: Also read the linked stores' indexes, their ids qualified by name.
    exclude_tags: Documents carrying one of these tags are left out (their nodes, their
        sections, their edges); the index itself holds everything.

Returns:
    The composed index; shared between callers, so treat it as read-only.

## Imports

["__future__", "pathlib", "sldb.store.edge_index.composition_targets", "sldb.store.edge_index.edge_index", "sldb.store.edge_index.federation", "sldb.store.edge_index.resolve", "sldb.store.edge_index.shard_reading", "sldb.store.edge_index.shard_signature", "sldb.store.io", "sldb.store.models", "typing"]

## Purpose

The store's edge index, read from its shards (never rebuilt here).

## Architecture

Not documented.
