---
id: python-sldb-sldb-store-edge_index-resolve-_onto_relation_type_nodes
system: sldb
module: sldb.store.edge_index.resolve
qualname: _onto_relation_type_nodes
kind: FunctionDef
source_path: sldb/store/edge_index/resolve.py
source_span: 64:74
source_sha256: b11aa99784a951e5c12b09b6ab1947d62243d1b715e6b23b15952d497976d90d
architecture_spec: Not declared.
tags: []
provenance: python-ast:python:sldb.store.edge_index.resolve:_onto_relation_type_nodes;
  contract-sha256:d9fad475e09023614c17b5a010fae6efde93c4aed4430472e303c9b8cdf3e8b1
---

# _onto_relation_type_nodes

## Signature

_onto_relation_type_nodes(nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord])

## Docstring

Edges whose end is a RelationTypeDoc's export id, pointed at its `relation_type` node.

A reference field holding `RelationTypeDoc:<doc>` names a tracked document, but the index
holds that document as `sldb://relation_type/<payload name>`, so the edge used to dangle
and be dropped in silence while `doc_exists` said the target was there.

## Imports

["__future__", "sldb.store.edge_index.declared_resolution", "sldb.store.edge_index.node_ids", "sldb.store.edge_index.unresolved_reference", "sldb.store.models", "typing"]

## Purpose

Edges whose end is a RelationTypeDoc's export id, pointed at its `relation_type` node.

## Architecture

Not documented.
