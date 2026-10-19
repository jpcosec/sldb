---
id: python-sldb-sldb-store-edge_index-federation-qualify_id
system: sldb
module: sldb.store.edge_index.federation
qualname: qualify_id
kind: FunctionDef
source_path: sldb/store/edge_index/federation.py
source_span: '27:38'
source_sha256: 8035b477af7ddc4e0a2a164daecf0883269b3012570643e3bb3e6591795e78c9
architecture_spec: docs/architecture/spec2viz/python-ast.yml; sha256=cece0196cfdf01c39315c3221d5fbe10e2953377809b62cfa800c0463d2146fd
tags: []
provenance: python-ast:python:sldb.store.edge_index.federation:qualify_id; contract-sha256:f0efdc3a14cef9bee780f7b2760733321c5ee3e7b105d6e381c8dc03efd3b097
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

The id as read from a linked store's shard, made absolute: documents and sections get the store's name unless they already name a store; models, fields, tags, relation types and anchors are one vocabulary across stores and stay as they are.

## Architecture

Not documented.
