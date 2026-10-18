---
id: python-sldb-sldb-sldb-store-edge_index-federation-qualify_id
system: sldb
module: sldb.sldb.store.edge_index.federation
qualname: qualify_id
kind: FunctionDef
source_path: sldb/store/edge_index/federation.py
source_span: '27:38'
source_sha256: 8035b477af7ddc4e0a2a164daecf0883269b3012570643e3bb3e6591795e78c9
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.sldb.store.edge_index.federation:qualify_id; contract-sha256:cb08b4b6c3b8d352dad1a1bd1af70f9928a49734b1f9a042474d2782e777f54c
---

# qualify_id

## Signature

qualify_id(node_id: str, store_name: str | None)

## Docstring

The id as read from a linked store's shard, made absolute: documents and sections get
the store's name unless they already name a store; models, fields, tags, relation types
and anchors are one vocabulary across stores and stay as they are.

## Imports

["__future__", "pathlib", "sldb.store.edge_index.node_ids", "sldb.store.models"]

## Purpose

Not documented.

## Architecture

Not documented.
